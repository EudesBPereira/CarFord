from sqlalchemy import Column, Integer, String, ForeignKey
from shared.database import Base

class Car(Base):
    __tablename__ = 'TB_CAR'
    __table_args__ = {'schema': 'dbo'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('dbo.TB_CUSTOMER.id'), nullable=False)
    color = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Car(id={self.id}, color={self.color}, model={self.model}, owner_id={self.owner_id})>"
