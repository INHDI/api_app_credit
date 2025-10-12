# Hướng dẫn Tính Toán Lãi Suất

## Khái niệm Lãi Suất trong Hệ Thống

Trong hệ thống này, **LaiSuat** (Lãi suất) là **số tiền cố định** (VNĐ) phải trả **mỗi kỳ đóng**, không phải là phần trăm (%).

### Ví dụ:
- `LaiSuat = 50000` nghĩa là **50,000 VNĐ** lãi mỗi kỳ đóng
- `LaiSuat = 100000` nghĩa là **100,000 VNĐ** lãi mỗi kỳ đóng

## Công Thức Tính Toán

### 1. Tiền Trả Mỗi Kỳ
```
Tiền trả mỗi kỳ = (Số tiền vay ÷ Số kỳ đóng) + Lãi suất
```

**Ví dụ:**
- Số tiền vay: 10,000,000 VNĐ
- Kỳ đóng: 12 tháng
- Lãi suất: 50,000 VNĐ/kỳ

```
Tiền trả mỗi kỳ = (10,000,000 ÷ 12) + 50,000
                = 833,333 + 50,000
                = 883,333 VNĐ
```

### 2. Tổng Tiền Phải Trả
```
Tổng tiền = Số tiền vay + (Lãi suất × Số kỳ đóng)
```

**Ví dụ:**
```
Tổng tiền = 10,000,000 + (50,000 × 12)
          = 10,000,000 + 600,000
          = 10,600,000 VNĐ
```

### 3. Số Tiền Còn Lại
```
Số tiền còn lại = Tổng tiền phải trả - Số tiền đã trả
```

**Ví dụ:**
- Tổng tiền phải trả: 10,600,000 VNĐ
- Đã trả: 2,000,000 VNĐ

```
Số tiền còn lại = 10,600,000 - 2,000,000
                = 8,600,000 VNĐ
```

## Ví Dụ Thực Tế

### Kịch Bản 1: Vay Tín Chấp
```json
{
  "HoTen": "Nguyễn Văn A",
  "SoTienVay": 10000000,
  "KyDong": 12,
  "LaiSuat": 50000
}
```

**Kế hoạch thanh toán:**
- Tháng 1-12: Mỗi tháng trả 883,333 VNĐ (gốc + lãi)
- Tổng lãi phải trả: 600,000 VNĐ (50,000 × 12)
- Tổng tiền: 10,600,000 VNĐ

### Kịch Bản 2: Vay Trả Góp
```json
{
  "HoTen": "Trần Thị B",
  "SoTienVay": 20000000,
  "KyDong": 24,
  "LaiSuat": 100000
}
```

**Kế hoạch thanh toán:**
- Tháng 1-24: Mỗi tháng trả 933,333 VNĐ (gốc + lãi)
- Tổng lãi phải trả: 2,400,000 VNĐ (100,000 × 24)
- Tổng tiền: 22,400,000 VNĐ

## Sử Dụng Utility Functions

```python
from app.utils import (
    calculate_monthly_payment,
    calculate_total_payment,
    calculate_remaining_amount
)

# Tính tiền trả hàng tháng
monthly = calculate_monthly_payment(
    principal=10000000,      # Số tiền vay
    interest_amount=50000,   # Lãi cố định mỗi kỳ
    months=12                # Số tháng
)
print(f"Trả mỗi tháng: {monthly:,} VNĐ")

# Tính tổng tiền phải trả
total = calculate_total_payment(
    principal=10000000,
    interest_amount=50000,
    months=12
)
print(f"Tổng: {total:,} VNĐ")

# Tính số tiền còn lại
remaining = calculate_remaining_amount(
    principal=10000000,
    interest_amount=50000,
    months=12,
    paid_amount=2000000      # Đã trả
)
print(f"Còn lại: {remaining:,} VNĐ")
```

## Lưu Ý

1. **Lãi suất là số tiền cố định**, không phải phần trăm
2. Lãi suất được tính **cho mỗi kỳ đóng** (thường là tháng)
3. Số tiền gốc được chia đều cho các kỳ
4. Lãi được cộng thêm vào mỗi kỳ
5. Tổng lãi = `LaiSuat × KyDong`

