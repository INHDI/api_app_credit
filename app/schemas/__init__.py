"""
Pydantic schemas package
"""
from app.schemas.tin_chap import (
    TinChapCreate,
    TinChapUpdate
)
from app.schemas.tra_gop import (
    TraGopCreate,
    TraGopUpdate
)
from app.schemas.lich_su_tra_lai import (
    LichSuTraLaiCreate,
    LichSuTraLaiUpdate
)
from app.schemas.response import ApiResponse

__all__ = [
    # TinChap
    "TinChapCreate",
    "TinChapUpdate",
    # TraGop
    "TraGopCreate",
    "TraGopUpdate",
    # LichSuTraLai
    "LichSuTraLaiCreate",
    "LichSuTraLaiUpdate",
    # Response
    "ApiResponse",
]

