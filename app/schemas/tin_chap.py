"""
TinChap schemas for API request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional


class TinChapCreate(BaseModel):
    """Schema for creating TinChap"""
    HoTen: str = Field(..., description="Họ tên người vay")
    NgayVay: date = Field(..., description="Ngày vay")
    SoTienVay: int = Field(..., gt=0, description="Số tiền vay")
    KyDong: int = Field(..., gt=0, description="Kỳ đóng (số ngày giữa các kỳ thanh toán)")
    LaiSuat: int = Field(..., ge=0, description="Lãi suất (số tiền cố định mỗi kỳ, VNĐ)")


class TinChapUpdate(BaseModel):
    """Schema for updating TinChap"""
    HoTen: Optional[str] = None
    NgayVay: Optional[date] = None
    SoTienVay: Optional[int] = None
    KyDong: Optional[int] = None
    LaiSuat: Optional[int] = None
    TrangThai: Optional[str] = None


class TinChap(BaseModel):
    """Schema for TinChap response - can serialize from SQLAlchemy model"""
    MaHD: str = Field(..., description="Mã hợp đồng")
    HoTen: str = Field(..., description="Họ tên người vay")
    NgayVay: date = Field(..., description="Ngày vay")
    SoTienVay: int = Field(..., description="Số tiền vay")
    KyDong: int = Field(..., description="Kỳ đóng (số ngày giữa các kỳ thanh toán)")
    LaiSuat: int = Field(..., description="Lãi suất (số tiền cố định mỗi kỳ, VNĐ)")
    TrangThai: str = Field(..., description="Trạng thái")
    
    model_config = ConfigDict(from_attributes=True)
