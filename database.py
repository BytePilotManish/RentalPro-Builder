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
    output_dir = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    agreements = relationship("Agreement", back_populates="owner", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    templates = relationship("Template", back_populates="user", cascade="all, delete-orphan")
    tenants = relationship("Tenant", back_populates="user", cascade="all, delete-orphan")
    owners = relationship("Owner", back_populates="user", cascade="all, delete-orphan")
    properties = relationship("Property", back_populates="user", cascade="all, delete-orphan")

class Agreement(Base):
    __tablename__ = "agreements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=True)
    title = Column(String, nullable=False)
    agreement_data = Column(Text, nullable=False)  # Stored as JSON string
    docx_path = Column(String, nullable=True)
    pdf_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="agreements")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=True)
    desc = Column(String, nullable=True)
    title_key = Column(String, nullable=True)
    desc_key = Column(String, nullable=True)
    params = Column(Text, nullable=True)  # Stored as JSON string of params dict
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    content = Column(Text, nullable=False)  # The raw text template with placeholders
    placeholders = Column(Text, nullable=False)  # JSON list of extracted placeholders, e.g. ["OWNER_NAME", "TENANT_NAME"]
    file_path = Column(String, nullable=True)  # Path to uploaded docx template
    has_file = Column(Integer, default=0)  # 0 = false, 1 = true
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="templates")

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    guardian = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    address = Column(Text, nullable=True)
    aadhar = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="tenants")

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    guardian = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="owners")

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    address = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    business_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="properties")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


