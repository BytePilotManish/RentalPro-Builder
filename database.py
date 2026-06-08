import os
from pathlib import Path
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from runtime_paths import data_dir

# Store the SQLite database in a writable location (works inside a packaged .exe too)
DB_PATH = os.path.join(data_dir(), "database.db")
DATABASE_URL = "sqlite:///" + Path(DB_PATH).as_posix()

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    master_conditions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    agreements = relationship("Agreement", back_populates="owner", cascade="all, delete-orphan")

class Agreement(Base):
    __tablename__ = "agreements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    agreement_data = Column(Text, nullable=False)  # Stored as JSON string
    docx_path = Column(String, nullable=True)
    pdf_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="agreements")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
