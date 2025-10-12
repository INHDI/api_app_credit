"""
CRUD operations for LichSuTraLai
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.lich_su_tra_lai import LichSuTraLai
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


def create_lich_su(db: Session, lich_su: LichSuTraLaiCreate) -> LichSuTraLai:
    """
    Create a new payment history record
    
    Args:
        db: Database session
        lich_su: Payment history creation data
        
    Returns:
        Created LichSuTraLai object
    """
    db_lich_su = LichSuTraLai(
        MaHD=lich_su.MaHD,
        Ngay=lich_su.Ngay,
        SoTien=lich_su.SoTien,
        NoiDung=lich_su.NoiDung,
        TrangThai=lich_su.TrangThai,
        TienDaTra=lich_su.TienDaTra
    )
    
    db.add(db_lich_su)
    db.commit()
    db.refresh(db_lich_su)
    
    return db_lich_su


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

