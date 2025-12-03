from datetime import datetime

from sqlalchemy import Column, Integer, Text, DateTime

from config.database.session import Base


class ConsultORM(Base):
    __tablename__ = "consults"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    original_text = Column(Text, nullable=False)
    analysis_json = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
