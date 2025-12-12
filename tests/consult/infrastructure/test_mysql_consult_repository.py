import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.consult.domain.consult_session import ConsultSession
from app.consult.domain.message import Message
from app.consult.infrastructure.model.consult_session_model import ConsultSessionModel
from app.consult.infrastructure.repository.mysql_consult_repository import MySQLConsultRepository
from app.shared.vo.mbti import MBTI
from app.shared.vo.gender import Gender
from config.database import Base


@pytest.fixture(scope="function")
def db_session():
    """테스트용 인메모리 SQLite DB 세션"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def repository(db_session):
    """MySQLConsultRepository 인스턴스"""
    return MySQLConsultRepository(db_session)


def test_save_and_find_session_by_id(repository, db_session):
    """세션을 저장하고 조회할 수 있다 (영속성 검증)"""
    # Given: 유효한 ConsultSession
    session = ConsultSession(
        id="session-123",
        user_id="user-456",
        mbti=MBTI("INTJ"),
        gender=Gender("MALE"),
        created_at=datetime(2024, 1, 15, 10, 30, 0),
    )

    # When: 세션을 저장하고
    repository.save(session)

    # Then: 같은 ID로 조회하면 동일한 데이터가 반환된다
    found = repository.find_by_id("session-123")
    assert found is not None
    assert found.id == "session-123"
    assert found.user_id == "user-456"
    assert found.mbti.value == "INTJ"
    assert found.gender.value == "MALE"
    assert found.created_at == datetime(2024, 1, 15, 10, 30, 0)


def test_find_nonexistent_session_returns_none(repository):
    """존재하지 않는 세션을 조회하면 None이 반환된다"""
    # When: 존재하지 않는 세션을 조회하면
    found = repository.find_by_id("nonexistent-id")

    # Then: None이 반환된다
    assert found is None


def test_persistence_after_session_restart(db_session):
    """세션 재시작 후에도 데이터가 유지된다 (영속성 검증)"""
    # Given: 세션을 저장하고
    repository = MySQLConsultRepository(db_session)
    session = ConsultSession(
        id="session-999",
        user_id="user-888",
        mbti=MBTI("ENFP"),
        gender=Gender("FEMALE"),
    )
    repository.save(session)

    # When: 새로운 repository 인스턴스를 생성하고
    new_repository = MySQLConsultRepository(db_session)

    # Then: 저장된 데이터를 조회할 수 있다
    found = new_repository.find_by_id("session-999")
    assert found is not None
    assert found.user_id == "user-888"
    assert found.mbti.value == "ENFP"
    assert found.gender.value == "FEMALE"


def test_save_multiple_sessions(repository):
    """여러 세션을 저장하고 각각 조회할 수 있다"""
    # Given: 여러 세션을 저장하고
    session1 = ConsultSession(
        id="session-1",
        user_id="user-1",
        mbti=MBTI("INTJ"),
        gender=Gender("MALE"),
    )
    session2 = ConsultSession(
        id="session-2",
        user_id="user-2",
        mbti=MBTI("ENFP"),
        gender=Gender("FEMALE"),
    )

    repository.save(session1)
    repository.save(session2)

    # When: 각각 조회하면
    found1 = repository.find_by_id("session-1")
    found2 = repository.find_by_id("session-2")

    # Then: 각각의 데이터가 정확히 반환된다
    assert found1.user_id == "user-1"
    assert found1.mbti.value == "INTJ"
    assert found2.user_id == "user-2"
    assert found2.mbti.value == "ENFP"


def test_save_session_with_messages(repository):
    """세션과 메시지를 함께 저장하고 조회할 수 있다"""
    # Given: 메시지가 있는 세션
    session = ConsultSession(
        id="session-with-messages",
        user_id="user-123",
        mbti=MBTI("INTJ"),
        gender=Gender("MALE"),
    )
    session.add_message(Message(role="user", content="안녕하세요"))
    session.add_message(Message(role="assistant", content="반갑습니다!"))

    # When: 세션을 저장하고 조회하면
    repository.save(session)
    found = repository.find_by_id("session-with-messages")

    # Then: 메시지도 함께 조회된다
    assert found is not None
    messages = found.get_messages()
    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[0].content == "안녕하세요"
    assert messages[1].role == "assistant"
    assert messages[1].content == "반갑습니다!"


def test_update_session_with_new_messages(repository):
    """기존 세션에 새 메시지를 추가하고 저장할 수 있다"""
    # Given: 메시지가 있는 세션을 저장하고
    session = ConsultSession(
        id="session-update",
        user_id="user-123",
        mbti=MBTI("ENFP"),
        gender=Gender("FEMALE"),
    )
    session.add_message(Message(role="user", content="첫 번째 메시지"))
    repository.save(session)

    # When: 세션을 조회하고 새 메시지를 추가하여 다시 저장하면
    found = repository.find_by_id("session-update")
    found.add_message(Message(role="assistant", content="AI 응답"))
    found.add_message(Message(role="user", content="두 번째 메시지"))
    repository.save(found)

    # Then: 모든 메시지가 저장되어 있다
    updated = repository.find_by_id("session-update")
    messages = updated.get_messages()
    assert len(messages) == 3
    assert messages[0].content == "첫 번째 메시지"
    assert messages[1].content == "AI 응답"
    assert messages[2].content == "두 번째 메시지"


def test_message_order_preserved(repository):
    """메시지 순서가 저장 및 조회 시 유지된다"""
    # Given: 여러 메시지가 있는 세션
    session = ConsultSession(
        id="session-order",
        user_id="user-123",
        mbti=MBTI("ISTP"),
        gender=Gender("MALE"),
    )
    for i in range(5):
        role = "user" if i % 2 == 0 else "assistant"
        session.add_message(Message(role=role, content=f"메시지 {i}"))

    # When: 저장하고 조회하면
    repository.save(session)
    found = repository.find_by_id("session-order")

    # Then: 메시지 순서가 유지된다
    messages = found.get_messages()
    assert len(messages) == 5
    for i, msg in enumerate(messages):
        assert msg.content == f"메시지 {i}"
