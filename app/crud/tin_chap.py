"""
CRUD operations for TinChap
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.tin_chap import TinChap
from app.schemas.tin_chap import TinChapCreate, TinChapUpdate
from app.core.enums import TrangThaiThanhToan


def get_tin_chap(db: Session, ma_hd: str) -> Optional[TinChap]:
    """
    Get a TinChap contract by MaHD
    
    Args:
        db: Database session
        ma_hd: Contract ID
        
    Returns:    
        TinChap object or None if not found
    """
    try:
        result = db.query(TinChap).filter(TinChap.MaHD == ma_hd).first()
        return result
    except Exception as e:
        raise


def get_tin_chaps(db: Session, skip: int = 0, limit: int = 100) -> List[TinChap]:
    """
    Get all TinChap contracts with pagination
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of TinChap objects
    """
    try:
        results = db.query(TinChap).offset(skip).limit(limit).all()
        return results
    except Exception as e:
        raise


def create_tin_chap(db: Session, tin_chap: TinChapCreate, ma_hd: str) -> TinChap:
    """
    Create a new TinChap contract
    
    Args:
        db: Database session
        tin_chap: TinChap creation data
        ma_hd: Generated contract ID
        
    Returns:
        Created TinChap object
    """
    try:
        trang_thai = TrangThaiThanhToan.CHUA_THANH_TOAN.value
        
        db_tin_chap = TinChap(
            MaHD=ma_hd,
            HoTen=tin_chap.HoTen,
            NgayVay=tin_chap.NgayVay,
            SoTienVay=tin_chap.SoTienVay,
            KyDong=tin_chap.KyDong,
            LaiSuat=tin_chap.LaiSuat,
            TrangThai=trang_thai
        )
        
        db.add(db_tin_chap)
        db.commit()
        db.refresh(db_tin_chap)
        
        return db_tin_chap
        
    except Exception as e:
        db.rollback()
        raise


def update_tin_chap(db: Session, ma_hd: str, tin_chap_update: TinChapUpdate) -> Optional[TinChap]:
    """
    Update a TinChap contract
    
    Args:
        db: Database session
        ma_hd: Contract ID
        tin_chap_update: Update data
        
    Returns:
        Updated TinChap object or None if not found
    """
    try:
        db_tin_chap = get_tin_chap(db, ma_hd)
        
        if not db_tin_chap:
            return None
        
        update_data = tin_chap_update.model_dump(exclude_unset=True)
        
        if update_data:
            for key, value in update_data.items():
                setattr(db_tin_chap, key, value)
            
            db.commit()
            db.refresh(db_tin_chap)
        
        return db_tin_chap
        
    except Exception as e:
        db.rollback()
        raise


def delete_tin_chap(db: Session, ma_hd: str) -> bool:
    """
    Delete a TinChap contract
    
    Args:
        db: Database session
        ma_hd: Contract ID
        
    Returns:
        True if deleted, False if not found
    """
    try:
        db_tin_chap = get_tin_chap(db, ma_hd)
        
        if not db_tin_chap:
            return False
        
        db.delete(db_tin_chap)
        db.commit()
        
        return True
        
    except Exception as e:
        db.rollback()
        raise


def get_tin_chaps_by_status(db: Session, trang_thai: str) -> List[TinChap]:
    """
    Get TinChap contracts by status
    
    Args:
        db: Database session
        trang_thai: Status to filter by
        
    Returns:
        List of TinChap objects
    """
    try:
        results = db.query(TinChap).filter(TinChap.TrangThai == trang_thai).all()
        return results
    except Exception as e:
        raise


def count_tin_chaps(db: Session) -> int:
    """
    Count total TinChap contracts
    
    Args:
        db: Database session
        
    Returns:
        Total count
    """
    try:
        count = db.query(TinChap).count()
        return count
    except Exception as e:
        raise

