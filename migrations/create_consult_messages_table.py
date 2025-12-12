"""
상담 메시지 테이블 생성 스크립트

실행 방법:
python migrations/create_consult_messages_table.py
"""

from config.database import engine, Base
from app.consult.infrastructure.model.consult_message_model import ConsultMessageModel


def create_tables():
    """consult_messages 테이블 생성"""
    print("Creating consult_messages table...")
    Base.metadata.create_all(bind=engine, tables=[ConsultMessageModel.__table__])
    print("✅ consult_messages table created successfully!")


if __name__ == "__main__":
    create_tables()