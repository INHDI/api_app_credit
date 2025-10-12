"""
Enums cho ứng dụng quản lý tín dụng
"""
from enum import Enum


class TrangThaiThanhToan(str, Enum):
    """Trạng thái thanh toán"""
    CHUA_THANH_TOAN = "Chưa thanh toán"
    DONG_DU = "Đóng đủ"
    THANH_TOAN_MOT_PHAN = "Thanh toán một phần"
    DEN_HAN_TRA_LAI = "Đến hạn trả lãi"
    QUA_HAN_TRA_LAI = "Quá hạn trả lãi"
    DA_TAT_TOAN = "Đã tất toán"
    
    @classmethod
    def list_values(cls):
        """Trả về danh sách tất cả các giá trị"""
        return [status.value for status in cls]

# Export all enums
__all__ = [
    "TrangThaiThanhToan", 
]

