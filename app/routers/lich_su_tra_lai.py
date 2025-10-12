"""
LichSuTraLai API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any

from app.core.database import get_db
from app.models import TinChap, TraGop
from app.schemas.lich_su_tra_lai import LichSuTraLaiCreate, LichSuTraLaiUpdate, LichSuTraLai
from app.schemas.response import ApiResponse
from app.crud import lich_su_tra_lai as crud_lich_su

router = APIRouter(
    prefix="/lich-su-tra-lai",
    tags=["Lịch sử trả lãi"]
)


@router.post("", response_model=ApiResponse[LichSuTraLai], status_code=201)
async def create_lich_su(lich_su: LichSuTraLaiCreate, db: Session = Depends(get_db)):
    """Create a new payment history record"""
    # Verify that MaHD exists in either TinChap or TraGop
    tin_chap = db.query(TinChap).filter(TinChap.MaHD == lich_su.MaHD).first()
    tra_gop = db.query(TraGop).filter(TraGop.MaHD == lich_su.MaHD).first()
    
    if not tin_chap and not tra_gop:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy hợp đồng {lich_su.MaHD}")
    
    result = crud_lich_su.create_lich_su(db=db, lich_su=lich_su)
    # Convert SQLAlchemy model to Pydantic schema
    lich_su_response = LichSuTraLai.model_validate(result)
    return ApiResponse.success_response(data=lich_su_response, message="Tạo lịch sử trả lãi thành công")


@router.get("", response_model=ApiResponse[List[LichSuTraLai]])
async def get_all_lich_su(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all payment history records"""
    result = crud_lich_su.get_lich_sus(db=db, skip=skip, limit=limit)
    # Convert list of SQLAlchemy models to Pydantic schemas
    lich_sus_response = [LichSuTraLai.model_validate(ls) for ls in result]
    return ApiResponse.success_response(data=lich_sus_response, message="Lấy danh sách lịch sử trả lãi thành công")


@router.get("/{stt}", response_model=ApiResponse[LichSuTraLai])
async def get_lich_su_by_id(stt: int, db: Session = Depends(get_db)):
    """Get a specific payment history record by STT"""
    lich_su = crud_lich_su.get_lich_su(db=db, stt=stt)
    if not lich_su:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch sử trả lãi")
    # Convert SQLAlchemy model to Pydantic schema
    lich_su_response = LichSuTraLai.model_validate(lich_su)
    return ApiResponse.success_response(data=lich_su_response, message="Lấy thông tin lịch sử trả lãi thành công")


@router.get("/contract/{ma_hd}", response_model=ApiResponse[List[LichSuTraLai]])
async def get_lich_su_by_contract(ma_hd: str, db: Session = Depends(get_db)):
    """Get all payment history records for a specific contract"""
    result = crud_lich_su.get_lich_sus_by_contract(db=db, ma_hd=ma_hd)
    # Convert list of SQLAlchemy models to Pydantic schemas
    lich_sus_response = [LichSuTraLai.model_validate(ls) for ls in result]
    return ApiResponse.success_response(data=lich_sus_response, message="Lấy lịch sử trả lãi theo hợp đồng thành công")


@router.put("/{stt}", response_model=ApiResponse[LichSuTraLai])
async def update_lich_su(stt: int, lich_su_update: LichSuTraLaiUpdate, db: Session = Depends(get_db)):
    """Update a payment history record"""
    db_lich_su = crud_lich_su.update_lich_su(db=db, stt=stt, lich_su_update=lich_su_update)
    if not db_lich_su:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch sử trả lãi")
    # Convert SQLAlchemy model to Pydantic schema
    lich_su_response = LichSuTraLai.model_validate(db_lich_su)
    return ApiResponse.success_response(data=lich_su_response, message="Cập nhật lịch sử trả lãi thành công")


@router.delete("/{stt}", response_model=ApiResponse[Any])
async def delete_lich_su(stt: int, db: Session = Depends(get_db)):
    """Delete a payment history record"""
    success = crud_lich_su.delete_lich_su(db=db, stt=stt)
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch sử trả lãi")
    return ApiResponse.success_response(data={"Stt": stt}, message="Xóa lịch sử trả lãi thành công")

