# API Testing Examples

Các ví dụ cURL để test API

## TinChap (Tín chấp)

### Tạo mới TinChap
```bash
curl -X POST "http://localhost:8080/tin-chap" \
  -H "Content-Type: application/json" \
  -d '{
    "HoTen": "Nguyen Van A",
    "NgayVay": "2025-10-12",
    "SoTienVay": 10000000,
    "KyDong": 12,
    "LaiSuat": 50000,
    "TrangThai": "Dang xu ly"
  }'
```
Note: LaiSuat = 50000 nghĩa là 50,000 VNĐ lãi mỗi kỳ đóng

### Lấy tất cả TinChap
```bash
curl -X GET "http://localhost:8080/tin-chap"
```

### Lấy TinChap theo mã
```bash
curl -X GET "http://localhost:8080/tin-chap/TC001"
```

### Cập nhật TinChap
```bash
curl -X PUT "http://localhost:8080/tin-chap/TC001" \
  -H "Content-Type: application/json" \
  -d '{
    "TrangThai": "Da duyet"
  }'
```

### Xóa TinChap
```bash
curl -X DELETE "http://localhost:8080/tin-chap/TC001"
```

## TraGop (Trả góp)

### Tạo mới TraGop
```bash
curl -X POST "http://localhost:8080/tra-gop" \
  -H "Content-Type: application/json" \
  -d '{
    "HoTen": "Tran Thi B",
    "NgayVay": "2025-10-12",
    "SoTienVay": 20000000,
    "KyDong": 24,
    "SoLanTra": 0,
    "LaiSuat": 100000,
    "TrangThai": "Dang hoat dong"
  }'
```
Note: LaiSuat = 100000 nghĩa là 100,000 VNĐ lãi mỗi kỳ đóng

### Lấy tất cả TraGop
```bash
curl -X GET "http://localhost:8080/tra-gop"
```

### Lấy TraGop theo mã
```bash
curl -X GET "http://localhost:8080/tra-gop/TG001"
```

### Cập nhật TraGop
```bash
curl -X PUT "http://localhost:8080/tra-gop/TG001" \
  -H "Content-Type: application/json" \
  -d '{
    "SoLanTra": 5,
    "TrangThai": "Dang thanh toan"
  }'
```

### Xóa TraGop
```bash
curl -X DELETE "http://localhost:8080/tra-gop/TG001"
```

## LichSuTraLai (Lịch sử trả lãi)

### Tạo mới lịch sử trả lãi
```bash
curl -X POST "http://localhost:8080/lich-su-tra-lai" \
  -H "Content-Type: application/json" \
  -d '{
    "MaHD": "TC001",
    "Ngay": "2025-10-12",
    "SoTien": 1000000,
    "NoiDung": "Tra goc va lai ky 1",
    "TrangThai": "Da thanh toan",
    "TienDaTra": "1000000"
  }'
```

### Lấy tất cả lịch sử
```bash
curl -X GET "http://localhost:8080/lich-su-tra-lai"
```

### Lấy lịch sử theo STT
```bash
curl -X GET "http://localhost:8080/lich-su-tra-lai/1"
```

### Lấy lịch sử theo mã hợp đồng
```bash
curl -X GET "http://localhost:8080/lich-su-tra-lai/contract/TC001"
```

### Cập nhật lịch sử
```bash
curl -X PUT "http://localhost:8080/lich-su-tra-lai/1" \
  -H "Content-Type: application/json" \
  -d '{
    "TrangThai": "Da xac nhan"
  }'
```

### Xóa lịch sử
```bash
curl -X DELETE "http://localhost:8080/lich-su-tra-lai/1"
```

## Python Examples

### Sử dụng requests library
```python
import requests
from datetime import date

BASE_URL = "http://localhost:8080"

# Tạo TinChap
tin_chap_data = {
    "HoTen": "Nguyen Van A",
    "NgayVay": str(date.today()),
    "SoTienVay": 10000000,
    "KyDong": 12,
    "LaiSuat": 50000,  # 50,000 VNĐ lãi mỗi kỳ
    "TrangThai": "Dang xu ly"
}

response = requests.post(f"{BASE_URL}/tin-chap", json=tin_chap_data)
print(response.json())

# Lấy tất cả TinChap
response = requests.get(f"{BASE_URL}/tin-chap")
print(response.json())

# Tính toán: Tổng tiền phải trả = SoTienVay + (LaiSuat * KyDong)
# Ví dụ: 10,000,000 + (50,000 * 12) = 10,600,000 VNĐ
```

