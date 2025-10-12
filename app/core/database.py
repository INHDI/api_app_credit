"""
Database configuration and session management
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join(BASE_DIR, "credit_app.sqlite3")

# SQLite database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create engine
# check_same_thread=False is needed for SQLite with FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Set to True to see SQL queries in console
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


# Dependency to get DB session
def get_db():
    """
    Get database session
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to initialize database
def init_db():
    """
    Initialize database - create all tables
    """
    # Import all models to ensure they are registered with Base
    from app.models import TinChap, TraGop, LichSuTraLai
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized at: {DATABASE_PATH}")
    print(f"✅ Tables created: tin_chap, tra_gop, lich_su_tra_lai")


# Function to drop all tables (use with caution!)
def drop_db():
    """
    Drop all tables - USE WITH CAUTION!
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️  All tables dropped!")

