"""
CRUD operations for TraGop
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.tra_gop import TraGop
from app.schemas.tra_gop import TraGopCreate, TraGopUpdate


def get_tra_gop(db: Session, ma_hd: str) -> Optional[TraGop]:
    """
    Get a TraGop contract by MaHD
    
    Args:
        db: Database session
        ma_hd: Contract ID
        
    Returns:
        TraGop object or None if not found
    """
    return db.query(TraGop).filter(TraGop.MaHD == ma_hd).first()


def get_tra_gops(db: Session, skip: int = 0, limit: int = 100) -> List[TraGop]:
    """
    Get all TraGop contracts with pagination
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of TraGop objects
    """
    return db.query(TraGop).offset(skip).limit(limit).all()


def create_tra_gop(db: Session, tra_gop: TraGopCreate, ma_hd: str) -> TraGop:
    """
    Create a new TraGop contract
    
    Args:
        db: Database session
        tra_gop: TraGop creation data
        ma_hd: Generated contract ID
        
    Returns:
        Created TraGop object
    """
    db_tra_gop = TraGop(
        MaHD=ma_hd,
        HoTen=tra_gop.HoTen,
        NgayVay=tra_gop.NgayVay,
        SoTienVay=tra_gop.SoTienVay,
        KyDong=tra_gop.KyDong,
        SoLanTra=tra_gop.SoLanTra,
        LaiSuat=tra_gop.LaiSuat,
        TrangThai=tra_gop.TrangThai
    )
    
    db.add(db_tra_gop)
    db.commit()
    db.refresh(db_tra_gop)
    
    return db_tra_gop


def update_tra_gop(db: Session, ma_hd: str, tra_gop_update: TraGopUpdate) -> Optional[TraGop]:
    """
    Update a TraGop contract
    
    Args:
        db: Database session
        ma_hd: Contract ID
        tra_gop_update: Update data
        
    Returns:
        Updated TraGop object or None if not found
    """
    db_tra_gop = get_tra_gop(db, ma_hd)
    
    if not db_tra_gop:
        return None
    
    update_data = tra_gop_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tra_gop, key, value)
    
    db.commit()
    db.refresh(db_tra_gop)
    
    return db_tra_gop


def delete_tra_gop(db: Session, ma_hd: str) -> bool:
    """
    Delete a TraGop contract
    
    Args:
        db: Database session
        ma_hd: Contract ID
        
    Returns:
        True if deleted, False if not found
    """
    db_tra_gop = get_tra_gop(db, ma_hd)
    
    if not db_tra_gop:
        return False
    
    db.delete(db_tra_gop)
    db.commit()
    
    return True


def get_tra_gops_by_status(db: Session, trang_thai: str) -> List[TraGop]:
    """
    Get TraGop contracts by status
    
    Args:
        db: Database session
        trang_thai: Status to filter by
        
    Returns:
        List of TraGop objects
    """
    return db.query(TraGop).filter(TraGop.TrangThai == trang_thai).all()


def count_tra_gops(db: Session) -> int:
    """
    Count total TraGop contracts
    
    Args:
        db: Database session
        
    Returns:
        Total count
    """
    return db.query(TraGop).count()

