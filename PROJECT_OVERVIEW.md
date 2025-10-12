# API App Credit - Project Overview

## 🎯 Overview

API App Credit là một ứng dụng quản lý tín dụng được xây dựng với FastAPI, SQLite, và SQLAlchemy. Ứng dụng hỗ trợ hai loại hình thức vay: **Tín chấp** (TinChap) và **Trả góp** (TraGop), cùng với quản lý lịch sử thanh toán.

## 📊 Core Features

### 1. Tín Chấp (TinChap)
- Vay không cần tài sản thế chấp
- Tự động sinh mã hợp đồng (TC001, TC002, ...)
- Quản lý thông tin người vay
- Theo dõi trạng thái hợp đồng

### 2. Trả Góp (TraGop)
- Vay trả góp theo kỳ
- Tự động sinh mã hợp đồng (TG001, TG002, ...)
- Theo dõi số lần đã trả
- Quản lý lịch sử thanh toán

### 3. Lịch Sử Trả Lãi (LichSuTraLai)
- Ghi nhận mọi giao dịch thanh toán
- Liên kết với hợp đồng TinChap hoặc TraGop
- Theo dõi tổng tiền đã trả

## 🏗️ Architecture

### Layered Architecture

```
┌─────────────────────────────────────┐
│         Client (API Requests)       │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│      Routers (API Endpoints)        │  ← Route layer
│  - tin_chap.py                      │
│  - tra_gop.py                       │
│  - lich_su_tra_lai.py               │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│       Schemas (Validation)          │  ← Validation layer
│  - Request validation               │
│  - Response serialization           │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│    Services (Business Logic)        │  ← Business layer (future)
│  - Complex operations               │
│  - Multi-model logic                │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│      Models (Database Layer)        │  ← Data layer
│  - SQLAlchemy ORM                   │
│  - Database operations              │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│       SQLite Database               │
└─────────────────────────────────────┘
```

## 📁 Directory Structure

```
app/
├── core/           → Core configuration (database, settings)
├── models/         → Database models (ORM)
├── schemas/        → Pydantic models (validation)
├── routers/        → API endpoints (routes)
├── services/       → Business logic (future expansion)
└── utils/          → Helper functions
    ├── id_generator.py    → Generate unique IDs
    └── calculations.py    → Financial calculations
```

## 🔄 Request Flow Example

### Creating a TinChap Contract

```python
# 1. Client sends POST request to /tin-chap
{
    "HoTen": "Nguyen Van A",
    "NgayVay": "2025-10-12",
    "SoTienVay": 10000000,
    "KyDong": 12,
    "LaiSuat": 50000,
    "TrangThai": "Dang xu ly"
}

# 2. Router (routers/tin_chap.py) receives request
#    - Validates using TinChapCreate schema
#    - Generates ID using generate_tin_chap_id()

# 3. Creates TinChap model instance
db_tin_chap = TinChap(MaHD="TC001", ...)

# 4. Saves to database
db.add(db_tin_chap)
db.commit()

# 5. Returns response using TinChapResponse schema
{
    "MaHD": "TC001",
    "HoTen": "Nguyen Van A",
    "SoTienVay": 10000000,
    ...
}
```

## 💡 Key Design Decisions

### 1. **Lãi Suất (Interest Rate)**
- **Lãi suất là số tiền cố định (VNĐ), KHÔNG phải phần trăm (%)**
- Ví dụ: `LaiSuat = 50000` = 50,000 VNĐ mỗi kỳ
- Công thức: `Tổng tiền = SoTienVay + (LaiSuat × KyDong)`

### 2. **ID Generation**
- Auto-increment with prefix
- TinChap: TC001, TC002, TC003, ...
- TraGop: TG001, TG002, TG003, ...

### 3. **Polymorphic Relationships**
- LichSuTraLai can relate to both TinChap and TraGop
- Uses MaHD as foreign key reference

### 4. **Separation of Concerns**
- Each model in separate file
- Each router handles one resource
- Clear responsibility boundaries

## 🚀 API Endpoints Summary

### TinChap
- `POST   /tin-chap` - Create new contract
- `GET    /tin-chap` - List all contracts
- `GET    /tin-chap/{ma_hd}` - Get one contract
- `PUT    /tin-chap/{ma_hd}` - Update contract
- `DELETE /tin-chap/{ma_hd}` - Delete contract

### TraGop
- `POST   /tra-gop` - Create new contract
- `GET    /tra-gop` - List all contracts
- `GET    /tra-gop/{ma_hd}` - Get one contract
- `PUT    /tra-gop/{ma_hd}` - Update contract
- `DELETE /tra-gop/{ma_hd}` - Delete contract

### LichSuTraLai
- `POST   /lich-su-tra-lai` - Create payment record
- `GET    /lich-su-tra-lai` - List all records
- `GET    /lich-su-tra-lai/{stt}` - Get one record
- `GET    /lich-su-tra-lai/contract/{ma_hd}` - Get by contract
- `PUT    /lich-su-tra-lai/{stt}` - Update record
- `DELETE /lich-su-tra-lai/{stt}` - Delete record

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.119.0+
- **Database**: SQLite
- **ORM**: SQLAlchemy 2.0+
- **Validation**: Pydantic 2.12+
- **Server**: Uvicorn
- **Package Manager**: uv

## 📚 Documentation Files

- `README.md` - Getting started guide
- `ARCHITECTURE.md` - Detailed architecture documentation
- `CALCULATION_GUIDE.md` - Interest calculation examples
- `PROJECT_OVERVIEW.md` - This file
- `test_api_examples.md` - API usage examples

## 🔐 Security Considerations (Future)

- [ ] Add authentication/authorization
- [ ] Implement rate limiting
- [ ] Add input sanitization
- [ ] Implement audit logging
- [ ] Add HTTPS in production

## 📈 Scalability Path

### Phase 1 (Current)
- Basic CRUD operations
- SQLite database
- In-process execution

### Phase 2 (Future)
- Add service layer
- Implement business logic
- Add validation rules
- Error handling improvements

### Phase 3 (Future)
- Switch to PostgreSQL
- Add caching (Redis)
- Implement background tasks
- Add monitoring/logging

### Phase 4 (Future)
- Microservices architecture
- API gateway
- Load balancing
- Containerization (Docker)

## 🧪 Testing Strategy (Future)

```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_schemas.py
│   └── test_utils.py
├── integration/
│   ├── test_tin_chap_api.py
│   ├── test_tra_gop_api.py
│   └── test_lich_su_api.py
└── e2e/
    └── test_complete_flow.py
```

## 💻 Development Workflow

1. **Add new feature**
   - Create model in `models/`
   - Create schemas in `schemas/`
   - Create router in `routers/`
   - Register router in `main.py`

2. **Modify existing feature**
   - Update model if schema changes
   - Update schemas if validation changes
   - Update router if endpoints change

3. **Add utility function**
   - Add to appropriate file in `utils/`
   - Export from `utils/__init__.py`

## 🎓 Learning Resources

- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Pydantic: https://docs.pydantic.dev/

## 📞 Support

For questions or issues, refer to:
1. API Documentation: `/docs` endpoint
2. Architecture guide: `ARCHITECTURE.md`
3. Examples: `test_api_examples.md`

