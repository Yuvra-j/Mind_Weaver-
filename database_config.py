# Database Configuration for MindWeaver
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/mindweaver')

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    picture_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")

class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    chat = relationship("Chat", back_populates="messages")

# Database utility functions
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)

def get_connection():
    """Get raw database connection for custom queries"""
    return psycopg2.connect(DATABASE_URL)

def get_cursor():
    """Get database cursor with dict-like results"""
    conn = get_connection()
    return conn.cursor(cursor_factory=RealDictCursor)

# Database operations
class DatabaseOperations:
    @staticmethod
    def create_user(google_id, email, name, picture_url=None):
        """Create a new user"""
        db = SessionLocal()
        try:
            user = User(
                google_id=google_id,
                email=email,
                name=name,
                picture_url=picture_url
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    @staticmethod
    def get_user_by_google_id(google_id):
        """Get user by Google ID"""
        db = SessionLocal()
        try:
            return db.query(User).filter(User.google_id == google_id).first()
        finally:
            db.close()
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        db = SessionLocal()
        try:
            return db.query(User).filter(User.email == email).first()
        finally:
            db.close()
    
    @staticmethod
    def create_chat(user_id, title=None):
        """Create a new chat"""
        db = SessionLocal()
        try:
            chat = Chat(user_id=user_id, title=title)
            db.add(chat)
            db.commit()
            db.refresh(chat)
            return chat
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    @staticmethod
    def get_user_chats(user_id, limit=10):
        """Get user's recent chats"""
        db = SessionLocal()
        try:
            return db.query(Chat).filter(Chat.user_id == user_id).order_by(Chat.updated_at.desc()).limit(limit).all()
        finally:
            db.close()
    
    @staticmethod
    def add_message(chat_id, role, content):
        """Add a message to a chat"""
        db = SessionLocal()
        try:
            message = Message(chat_id=chat_id, role=role, content=content)
            db.add(message)
            db.commit()
            db.refresh(message)
            return message
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    @staticmethod
    def get_chat_messages(chat_id):
        """Get all messages for a chat"""
        db = SessionLocal()
        try:
            return db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.created_at.asc()).all()
        finally:
            db.close()
    
    @staticmethod
    def get_chat_by_id(chat_id):
        """Get chat by ID"""
        db = SessionLocal()
        try:
            return db.query(Chat).filter(Chat.id == chat_id).first()
        finally:
            db.close()
