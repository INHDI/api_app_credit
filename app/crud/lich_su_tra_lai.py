"""
CRUD operations for LichSuTraLai
"""
from datetime import date, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.enums import TrangThaiThanhToan
from app.models.lich_su_tra_lai import LichSuTraLai
from app.models.tin_chap import TinChap
from app.models.tra_gop import TraGop
from app.schemas.lich_su_tra_lai import LichSuTraLaiCreate, LichSuTraLaiUpdate


def get_lich_su(db: Session, stt: int) -> Optional[LichSuTraLai]:
    """
    Get a payment history record by STT
    
    Args:
        db: Database session
        stt: Record ID
        
    Returns:
        LichSuTraLai object or None if not found
    """
    return db.query(LichSuTraLai).filter(LichSuTraLai.Stt == stt).first()


def get_lich_sus(db: Session, skip: int = 0, limit: int = 100) -> List[LichSuTraLai]:
    """
    Get all payment history records with pagination
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of LichSuTraLai objects
    """
    return db.query(LichSuTraLai).offset(skip).limit(limit).all()


def get_lich_sus_by_contract(db: Session, ma_hd: str) -> List[LichSuTraLai]:
    """
    Get payment history records by contract ID
    
    Args:
        db: Database session
        ma_hd: Contract ID
        
    Returns:
        List of LichSuTraLai objects
    """
    return db.query(LichSuTraLai).filter(LichSuTraLai.MaHD == ma_hd).all()


def create_lich_su(db: Session, ma_hd: str) -> dict:
    """
    Tạo các bản ghi lịch sử trả lãi dựa trên thông tin hợp đồng
    
    Logic:
    - Tín Chấp (TC): Mỗi kỳ trả = LaiSuat (chỉ trả lãi)
    - Trả Góp (TG): Mỗi kỳ trả = (SoTienVay + LaiSuat) / SoLanTra (trả cả gốc và lãi)
    - KyDong: Số ngày giữa các kỳ thanh toán
    - Nếu NgayVay < Ngày hiện tại: Tạo nhiều bản ghi với các kỳ cũ = 0, kỳ cuối = tổng cộng dồn
    - Nếu NgayVay = Ngày hiện tại: Không tạo bản ghi nào
    
    Args:
        db: Database session
        ma_hd: Mã hợp đồng (TCXXX hoặc TGXXX)
        
    Returns:
        dict: Thông tin thành công với số bản ghi đã tạo
    """
    try:
        # 1. Xác định loại hợp đồng và lấy dữ liệu
        loai_hop_dong = ""
        data_hop_dong = None
        
        if "TG" in ma_hd:
            loai_hop_dong = "TG"
            data_hop_dong = db.query(TraGop).filter(TraGop.MaHD == ma_hd).first()
        elif "TC" in ma_hd:
            loai_hop_dong = "TC"
            data_hop_dong = db.query(TinChap).filter(TinChap.MaHD == ma_hd).first()
        else:
            raise HTTPException(status_code=400, detail=f"Mã hợp đồng không hợp lệ: {ma_hd}")
        
        if not data_hop_dong:
            raise HTTPException(status_code=404, detail=f"Không tìm thấy hợp đồng {ma_hd}")
        
        # 2. Lấy thông tin từ hợp đồng
        ngay_vay = data_hop_dong.NgayVay
        ky_dong = data_hop_dong.KyDong  # Số ngày giữa các kỳ
        lai_suat = data_hop_dong.LaiSuat
        date_now = date.today()
        
        # 3. Kiểm tra nếu NgayVay = hôm nay → không tạo gì
        if ngay_vay >= date_now:
            return {
                "success": True,
                "message": "Ngày vay chưa đến hoặc là hôm nay, không cần tạo lịch sử",
                "records_created": 0
            }
        
        # 4. Tính số tiền mỗi kỳ dựa trên loại hợp đồng
        so_tien_moi_ky = 0
        if loai_hop_dong == "TC":
            # Tín Chấp: Mỗi kỳ chỉ trả lãi
            so_tien_moi_ky = lai_suat
        elif loai_hop_dong == "TG":
            # Trả Góp: Mỗi kỳ trả = (Gốc + Lãi) / Số lần trả
            so_tien_vay = data_hop_dong.SoTienVay
            so_lan_tra = data_hop_dong.SoLanTra
            if so_lan_tra <= 0:
                raise HTTPException(status_code=400, detail="SoLanTra phải lớn hơn 0")
            so_tien_moi_ky = (so_tien_vay + lai_suat) // so_lan_tra  # Làm tròn xuống
        
        # 5. Tính các kỳ thanh toán từ NgayVay đến hôm nay
        danh_sach_ky = []
        ngay_ky_hien_tai = ngay_vay + timedelta(days=ky_dong)  # Kỳ đầu tiên
        ky_thu = 1
        
        while ngay_ky_hien_tai <= date_now:
            danh_sach_ky.append({
                "ngay": ngay_ky_hien_tai,
                "ky_thu": ky_thu,
                "so_tien_ky": so_tien_moi_ky
            })
            ngay_ky_hien_tai += timedelta(days=ky_dong)
            ky_thu += 1
        
        # 6. Nếu không có kỳ nào
        if len(danh_sach_ky) == 0:
            return {
                "success": True,
                "message": "Chưa đến kỳ thanh toán đầu tiên",
                "records_created": 0
            }
        
        # 7. Tạo các bản ghi lịch sử
        so_ky = len(danh_sach_ky)
        tong_tien_cong_don = so_tien_moi_ky * so_ky  # Tổng tiền cộng dồn
        
        for idx, ky in enumerate(danh_sach_ky):
            # Các kỳ cũ: SoTien = 0
            # Kỳ cuối: SoTien = tổng cộng dồn
            so_tien = 0 if idx < len(danh_sach_ky) - 1 else tong_tien_cong_don
            
            db_lich_su = LichSuTraLai(
                MaHD=ma_hd,
                Ngay=ky["ngay"],
                SoTien=so_tien,
                NoiDung=f"Trả lãi kỳ {ky['ky_thu']}",
                TrangThai=TrangThaiThanhToan.QUA_HAN_TRA_LAI.value,
                TienDaTra=0
            )
            db.add(db_lich_su)
        
        # 8. Commit vào database
        db.commit()
        
        return {
            "success": True,
            "message": f"Đã tạo {so_ky} bản ghi lịch sử trả lãi",
            "records_created": so_ky,
            "loai_hop_dong": loai_hop_dong,
            "so_tien_moi_ky": so_tien_moi_ky,
            "tong_tien_cong_don": tong_tien_cong_don
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi khi tạo lịch sử: {str(e)}")


def update_lich_su(db: Session, stt: int, lich_su_update: LichSuTraLaiUpdate) -> Optional[LichSuTraLai]:
    """
    Update a payment history record
    
    Args:
        db: Database session
        stt: Record ID
        lich_su_update: Update data
        
    Returns:
        Updated LichSuTraLai object or None if not found
    """
    db_lich_su = get_lich_su(db, stt)
    
    if not db_lich_su:
        return None
    
    update_data = lich_su_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_lich_su, key, value)
    
    db.commit()
    db.refresh(db_lich_su)
    
    return db_lich_su


def delete_lich_su(db: Session, stt: int) -> bool:
    """
    Delete a payment history record
    
    Args:
        db: Database session
        stt: Record ID
        
    Returns:
        True if deleted, False if not found
    """
    db_lich_su = get_lich_su(db, stt)
    
    if not db_lich_su:
        return False
    
    db.delete(db_lich_su)
    db.commit()
    
    return True


def count_lich_sus(db: Session) -> int:
    """
    Count total payment history records
    
    Args:
        db: Database session
        
    Returns:
        Total count
    """
    return db.query(LichSuTraLai).count()


def count_lich_sus_by_contract(db: Session, ma_hd: str) -> int:
    """
    Count payment history records for a specific contract
    
    Args:
        db: Database session
        ma_hd: Contract ID
        
    Returns:
        Count of records
    """
    return db.query(LichSuTraLai).filter(LichSuTraLai.MaHD == ma_hd).count()

