"""
TraGop model - Trả góp (Installment payment)
"""
from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base
import datetime


class TraGop(Base):
    """
    Trả góp - Installment payment
    """
    __tablename__ = "tra_gop"

    MaHD = Column(String, primary_key=True, index=True)  # Format: TGXXX
    HoTen = Column(String, nullable=False)
    NgayVay = Column(Date, nullable=False, default=datetime.date.today)
    SoTienVay = Column(Integer, nullable=False)
    KyDong = Column(Integer, nullable=False)  # Payment period (months)
    SoLanTra = Column(Integer, nullable=False, default=0)  # Number of payments made
    LaiSuat = Column(Integer, nullable=False)  # Fixed interest amount (VNĐ)
    TrangThai = Column(String, nullable=False)  # Status

    def __repr__(self):
        return f"<TraGop(MaHD='{self.MaHD}', HoTen='{self.HoTen}', SoTienVay={self.SoTienVay})>"

