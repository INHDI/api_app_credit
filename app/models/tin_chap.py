"""
TinChap model - Tín chấp (Credit without collateral)
"""
from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base
import datetime


class TinChap(Base):
    """
    Tín chấp - Credit without collateral
    """
    __tablename__ = "tin_chap"

    MaHD = Column(String, primary_key=True, index=True)  # Format: TCXXX
    HoTen = Column(String, nullable=False)
    NgayVay = Column(Date, nullable=False, default=datetime.date.today)
    SoTienVay = Column(Integer, nullable=False)
    KyDong = Column(Integer, nullable=False)  # Payment period (months)
    LaiSuat = Column(Integer, nullable=False)  # Fixed interest amount (VNĐ)
    TrangThai = Column(String, nullable=False)  # Status

    def __repr__(self):
        return f"<TinChap(MaHD='{self.MaHD}', HoTen='{self.HoTen}', SoTienVay={self.SoTienVay})>"

