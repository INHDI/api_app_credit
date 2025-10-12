# Architecture Documentation

## Overview

This application follows a **layered architecture** pattern, separating concerns into distinct modules for better maintainability, scalability, and testability.

## Directory Structure

### 📁 `app/core/`
**Purpose**: Core configuration and shared utilities

- `database.py`: Database connection, session management, and Base model
- Contains database engine, SessionLocal, and dependency injection functions

**When to use**: 
- Adding new database configurations
- Modifying connection settings
- Adding global dependencies

---

### 📁 `app/models/`
**Purpose**: SQLAlchemy ORM models (Database layer)

Each file represents a database table:
- `tin_chap.py`: TinChap model
- `tra_gop.py`: TraGop model
- `lich_su_tra_lai.py`: LichSuTraLai model

**Responsibilities**:
- Define database schema
- Define relationships between tables
- Provide model representations

**When to add new file**:
- When creating a new database table
- Keep one model per file for clarity

---

### 📁 `app/schemas/`
**Purpose**: Pydantic models for request/response validation (API layer)

Each file corresponds to a model:
- `tin_chap.py`: TinChap schemas (Create, Update, Response)
- `tra_gop.py`: TraGop schemas
- `lich_su_tra_lai.py`: LichSuTraLai schemas

**Responsibilities**:
- Validate incoming API requests
- Serialize outgoing API responses
- Define data types and constraints

**Schema Types**:
- `*Base`: Shared fields
- `*Create`: Fields required for creation
- `*Update`: Optional fields for updates
- `*Response`: Fields returned in API response

---

### 📁 `app/routers/`
**Purpose**: API endpoint definitions (Route layer)

Each file handles endpoints for one resource:
- `tin_chap.py`: `/tin-chap` endpoints
- `tra_gop.py`: `/tra-gop` endpoints
- `lich_su_tra_lai.py`: `/lich-su-tra-lai` endpoints

**Responsibilities**:
- Define API routes (GET, POST, PUT, DELETE)
- Handle HTTP requests/responses
- Call appropriate services/database operations
- Return formatted responses

**Standard CRUD operations**:
- `POST /resource` - Create
- `GET /resource` - List all
- `GET /resource/{id}` - Get one
- `PUT /resource/{id}` - Update
- `DELETE /resource/{id}` - Delete

---

### 📁 `app/services/`
**Purpose**: Business logic layer (currently empty, for future use)

**When to add services**:
- Complex business logic that doesn't belong in routes
- Logic that needs to be reused across multiple endpoints
- Operations involving multiple models
- External API integrations

**Example use cases**:
```python
# app/services/credit_service.py
def calculate_payment_schedule(contract_id: str, db: Session):
    """Generate complete payment schedule for a contract"""
    # Complex logic here
    pass

def approve_credit_application(contract_id: str, db: Session):
    """Business logic for approving credit"""
    # Check requirements, update status, send notifications
    pass
```

---

### 📁 `app/utils/`
**Purpose**: Utility functions and helpers

- `id_generator.py`: Generate unique IDs for contracts
- `calculations.py`: Financial calculation functions

**Responsibilities**:
- Pure functions without side effects
- Reusable across the application
- No database dependencies (except id_generator)

**When to add utilities**:
- Common calculations
- Data transformation functions
- Validation helpers
- Format converters

---

## Data Flow

### Request Flow (Example: Create TinChap)

```
1. Client Request
   ↓
2. FastAPI (main.py)
   ↓
3. Router (routers/tin_chap.py)
   - Validates request using Schema (schemas/tin_chap.py)
   - Generates ID using Utils (utils/id_generator.py)
   ↓
4. Database Session (core/database.py)
   ↓
5. Model (models/tin_chap.py)
   - Creates database record
   ↓
6. Response
   - Serializes using Schema (schemas/tin_chap.py)
   - Returns to client
```

### With Services Layer (Future)

```
1. Client Request
   ↓
2. Router
   ↓
3. Service (business logic)
   ↓
4. Model (database operations)
   ↓
5. Response
```

---

## Design Principles

### 1. **Separation of Concerns**
Each layer has a specific responsibility:
- **Routers**: HTTP handling
- **Services**: Business logic
- **Models**: Data persistence
- **Schemas**: Data validation
- **Utils**: Helper functions

### 2. **Single Responsibility**
- One file per model/resource
- One function does one thing
- Clear naming conventions

### 3. **Dependency Injection**
```python
def endpoint(db: Session = Depends(get_db)):
    # Database session injected by FastAPI
    pass
```

### 4. **Type Safety**
- Pydantic schemas for validation
- Type hints throughout
- SQLAlchemy types in models

---

## Adding New Features

### Adding a New Model (e.g., "KhachHang")

1. **Create Model** (`app/models/khach_hang.py`)
```python
class KhachHang(Base):
    __tablename__ = "khach_hang"
    # fields...
```

2. **Create Schemas** (`app/schemas/khach_hang.py`)
```python
class KhachHangBase(BaseModel):
    # fields...

class KhachHangCreate(KhachHangBase):
    pass

class KhachHangResponse(KhachHangBase):
    id: int
    class Config:
        from_attributes = True
```

3. **Create Router** (`app/routers/khach_hang.py`)
```python
router = APIRouter(prefix="/khach-hang", tags=["KhachHang"])

@router.post("")
async def create_khach_hang(...):
    pass
```

4. **Register Router** (`app/main.py`)
```python
from app.routers import khach_hang
app.include_router(khach_hang.router)
```

5. **Add to `__init__.py`** files for easy imports

---

## Testing Strategy

### Unit Tests
- Test utils functions independently
- Test schemas validation
- Test model methods

### Integration Tests
- Test API endpoints
- Test database operations
- Test full request/response cycle

### Example:
```python
def test_create_tin_chap():
    response = client.post("/tin-chap", json={...})
    assert response.status_code == 201
    assert response.json()["MaHD"].startswith("TC")
```

---

## Best Practices

1. **Keep routers thin**: Move complex logic to services
2. **Use type hints**: Helps catch errors early
3. **Validate early**: Use Pydantic schemas
4. **One model per file**: Better organization
5. **Document complex logic**: Add docstrings
6. **Use consistent naming**: Follow Python conventions
7. **Handle errors gracefully**: Use HTTPException
8. **Log important events**: Use logging module (future)

---

## Future Enhancements

- [ ] Add service layer for business logic
- [ ] Implement authentication/authorization
- [ ] Add logging middleware
- [ ] Create unit and integration tests
- [ ] Add API versioning
- [ ] Implement caching
- [ ] Add background tasks (Celery)
- [ ] Add monitoring/metrics

