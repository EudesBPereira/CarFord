from sqlalchemy import Column, Integer, String
from shared.database import Base

class User(Base):
    __tablename__ = 'TB_USERS'
    __table_args__ = {'schema': 'dbo'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
