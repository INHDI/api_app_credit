"""
TinChap API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any

from app.core.database import get_db
from app.schemas.tin_chap import TinChapCreate, TinChapUpdate, TinChap
from app.schemas.response import ApiResponse
from app.crud import tin_chap as crud_tin_chap
from app.utils.id_generator import generate_tin_chap_id

router = APIRouter(
    prefix="/tin-chap",
    tags=["Tín chấp"]
)


@router.post("", response_model=ApiResponse[TinChap], status_code=201)
async def create_tin_chap(tin_chap: TinChapCreate, db: Session = Depends(get_db)):
    """Create a new TinChap contract"""
    ma_hd = generate_tin_chap_id(db)
    result = crud_tin_chap.create_tin_chap(db=db, tin_chap=tin_chap, ma_hd=ma_hd)
    # Convert SQLAlchemy model to Pydantic schema
    tin_chap_response = TinChap.model_validate(result)
    return ApiResponse.success_response(data=tin_chap_response, message="Tạo hợp đồng tín chấp thành công")


@router.get("", response_model=ApiResponse[List[TinChap]])
async def get_all_tin_chap(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
    ):
    """Get all TinChap contracts"""
    result = crud_tin_chap.get_tin_chaps(db=db, skip=skip, limit=limit)
    # Convert list of SQLAlchemy models to Pydantic schemas
    tin_chaps_response = [TinChap.model_validate(tc) for tc in result]
    return ApiResponse.success_response(data=tin_chaps_response, message="Lấy danh sách hợp đồng tín chấp thành công")


@router.get("/{ma_hd}", response_model=ApiResponse[TinChap])
async def get_tin_chap_by_id(ma_hd: str, db: Session = Depends(get_db)):
    """Get a specific TinChap contract by MaHD"""
    tin_chap = crud_tin_chap.get_tin_chap(db=db, ma_hd=ma_hd)
    if not tin_chap:
        raise HTTPException(status_code=404, detail="Không tìm thấy hợp đồng tín chấp")
    # Convert SQLAlchemy model to Pydantic schema
    tin_chap_response = TinChap.model_validate(tin_chap)
    return ApiResponse.success_response(data=tin_chap_response, message="Lấy thông tin hợp đồng tín chấp thành công")


@router.put("/{ma_hd}", response_model=ApiResponse[TinChap])
async def update_tin_chap(ma_hd: str, tin_chap_update: TinChapUpdate, db: Session = Depends(get_db)):
    """Update a TinChap contract"""
    db_tin_chap = crud_tin_chap.update_tin_chap(db=db, ma_hd=ma_hd, tin_chap_update=tin_chap_update)
    if not db_tin_chap:
        raise HTTPException(status_code=404, detail="Không tìm thấy hợp đồng tín chấp")
    # Convert SQLAlchemy model to Pydantic schema
    tin_chap_response = TinChap.model_validate(db_tin_chap)
    return ApiResponse.success_response(data=tin_chap_response, message="Cập nhật hợp đồng tín chấp thành công")


@router.delete("/{ma_hd}", response_model=ApiResponse[Any])
async def delete_tin_chap(ma_hd: str, db: Session = Depends(get_db)):
    """Delete a TinChap contract"""
    success = crud_tin_chap.delete_tin_chap(db=db, ma_hd=ma_hd)
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy hợp đồng tín chấp")
    return ApiResponse.success_response(data={"MaHD": ma_hd}, message="Xóa hợp đồng tín chấp thành công")

