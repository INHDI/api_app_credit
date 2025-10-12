# API App Credit

A FastAPI application for credit management system.

## Features

- Credit application submission
- Credit approval/rejection logic
- Application status tracking
- RESTful API endpoints

## Installation

This project uses `uv` for Python package management.

1. Make sure you have `uv` installed
2. Install dependencies:
   ```bash
   uv sync
   ```

## Project Structure

```
api_app_credit/
├── app/
│   ├── core/                    # Core configuration
│   │   ├── __init__.py
│   │   └── database.py         # Database configuration and session
│   ├── models/                  # SQLAlchemy database models
│   │   ├── __init__.py
│   │   ├── tin_chap.py         # TinChap model
│   │   ├── tra_gop.py          # TraGop model
│   │   └── lich_su_tra_lai.py  # LichSuTraLai model
│   ├── schemas/                 # Pydantic schemas for validation
│   │   ├── __init__.py
│   │   ├── tin_chap.py         # TinChap schemas
│   │   ├── tra_gop.py          # TraGop schemas
│   │   └── lich_su_tra_lai.py  # LichSuTraLai schemas
│   ├── routers/                 # API route handlers
│   │   ├── __init__.py
│   │   ├── tin_chap.py         # TinChap endpoints
│   │   ├── tra_gop.py          # TraGop endpoints
│   │   └── lich_su_tra_lai.py  # LichSuTraLai endpoints
│   ├── services/                # Business logic layer (future)
│   │   └── __init__.py
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   ├── id_generator.py     # ID generation utilities
│   │   └── calculations.py     # Financial calculations
│   ├── __init__.py
│   └── main.py                  # FastAPI application setup
├── main.py                      # Entry point
├── pyproject.toml              # Project configuration
├── uv.lock                     # Dependencies lock file
├── credit_app.db               # SQLite database (created on first run)
├── CALCULATION_GUIDE.md        # Interest calculation guide
├── test_api_examples.md        # API testing examples
└── README.md                   # This file
```

### Architecture Benefits

- **Separation of Concerns**: Each module has a specific responsibility
- **Scalability**: Easy to add new features without affecting existing code
- **Maintainability**: Clear structure makes code easier to understand and modify
- **Testability**: Isolated components are easier to test
- **Reusability**: Utils and services can be reused across different parts of the application

## Running the Application

### Option 1: Using the main entry point
```bash
uv run python main.py
```

### Option 2: Using the app run script
```bash
uv run python app/run.py
```

### Option 3: Using uvicorn directly
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## Lãi Suất (Interest Rate)

**Quan trọng:** Trong hệ thống này, `LaiSuat` là **số tiền cố định (VNĐ)** phải trả mỗi kỳ, **KHÔNG phải phần trăm (%)**.

### Ví dụ:
- `LaiSuat = 50000` → 50,000 VNĐ lãi mỗi kỳ đóng
- Vay 10,000,000 VNĐ, 12 kỳ, lãi 50,000 VNĐ/kỳ
- **Tổng lãi:** 50,000 × 12 = 600,000 VNĐ
- **Tổng phải trả:** 10,600,000 VNĐ

Xem chi tiết: [CALCULATION_GUIDE.md](CALCULATION_GUIDE.md)

## Database Models

### TinChap (Tín chấp - Credit without collateral)
- `MaHD`: Contract ID (Format: TCXXX - auto-generated)
- `HoTen`: Full name
- `NgayVay`: Loan date
- `SoTienVay`: Loan amount (VNĐ)
- `KyDong`: Payment period (months)
- `LaiSuat`: Fixed interest amount per period (VNĐ, e.g., 10 means 10 VNĐ per payment)
- `TrangThai`: Status

### TraGop (Trả góp - Installment payment)
- `MaHD`: Contract ID (Format: TGXXX - auto-generated)
- `HoTen`: Full name
- `NgayVay`: Loan date
- `SoTienVay`: Loan amount (VNĐ)
- `KyDong`: Payment period (months)
- `SoLanTra`: Number of payments made
- `LaiSuat`: Fixed interest amount per period (VNĐ, e.g., 10 means 10 VNĐ per payment)
- `TrangThai`: Status

### LichSuTraLai (Payment history)
- `Stt`: Auto-increment ID
- `MaHD`: Contract ID (from TinChap or TraGop)
- `Ngay`: Payment date
- `SoTien`: Payment amount
- `NoiDung`: Description
- `TrangThai`: Status
- `TienDaTra`: Total amount paid

## API Endpoints

### General
- `GET /` - Root endpoint
- `GET /health` - Health check

### TinChap Endpoints
- `POST /tin-chap` - Create new TinChap contract
- `GET /tin-chap` - Get all TinChap contracts
- `GET /tin-chap/{ma_hd}` - Get specific TinChap contract
- `PUT /tin-chap/{ma_hd}` - Update TinChap contract
- `DELETE /tin-chap/{ma_hd}` - Delete TinChap contract

### TraGop Endpoints
- `POST /tra-gop` - Create new TraGop contract
- `GET /tra-gop` - Get all TraGop contracts
- `GET /tra-gop/{ma_hd}` - Get specific TraGop contract
- `PUT /tra-gop/{ma_hd}` - Update TraGop contract
- `DELETE /tra-gop/{ma_hd}` - Delete TraGop contract

### LichSuTraLai Endpoints
- `POST /lich-su-tra-lai` - Create new payment history record
- `GET /lich-su-tra-lai` - Get all payment history records
- `GET /lich-su-tra-lai/{stt}` - Get specific payment history record
- `GET /lich-su-tra-lai/contract/{ma_hd}` - Get all payment history for a contract
- `PUT /lich-su-tra-lai/{stt}` - Update payment history record
- `DELETE /lich-su-tra-lai/{stt}` - Delete payment history record

## API Documentation

Once the server is running, visit:
- Interactive API docs: http://localhost:8080/docs
- Alternative docs: http://localhost:8080/redoc
