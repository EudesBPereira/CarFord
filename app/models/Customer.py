from sqlalchemy import Column, Integer, String, Boolean
from shared.database import Base

class Customer(Base):
    __tablename__ = 'TB_CUSTOMER'
    __table_args__ = {'schema': 'dbo'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(11), nullable=False)
    address = Column(String(255), nullable=True)
    has_opportunity = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Customer(id={self.id}, name={self.name}, email={self.email})>"
