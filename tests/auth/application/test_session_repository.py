import pytest
from app.auth.domain.session import Session
from app.auth.infrastructure.repository.in_memory_session_repository import (
    InMemorySessionRepository,
)


def test_save_and_find_session():
    """세션을 저장하고 session_id로 조회할 수 있다"""
    # Given: 저장소와 세션
    repository = InMemorySessionRepository()
    session = Session(session_id="session-123", user_id="user-456")

    # When: 세션을 저장하고 조회하면
    repository.save(session)
    found = repository.find_by_session_id("session-123")

    # Then: 동일한 세션을 반환한다
    assert found is not None
    assert found.session_id == "session-123"
    assert found.user_id == "user-456"


def test_find_nonexistent_session_returns_none():
    """존재하지 않는 session_id로 조회하면 None을 반환한다"""
    # Given: 빈 저장소
    repository = InMemorySessionRepository()

    # When: 존재하지 않는 세션을 조회하면
    found = repository.find_by_session_id("nonexistent")

    # Then: None을 반환한다
    assert found is None


def test_delete_session():
    """세션을 삭제할 수 있다"""
    # Given: 저장된 세션
    repository = InMemorySessionRepository()
    session = Session(session_id="session-123", user_id="user-456")
    repository.save(session)

    # When: 세션을 삭제하면
    repository.delete("session-123")

    # Then: 더 이상 조회되지 않는다
    assert repository.find_by_session_id("session-123") is None


def test_delete_nonexistent_session_does_not_raise():
    """존재하지 않는 세션 삭제 시 에러가 발생하지 않는다"""
    # Given: 빈 저장소
    repository = InMemorySessionRepository()

    # When & Then: 존재하지 않는 세션 삭제 시 에러 없음
    repository.delete("nonexistent")  # 에러가 발생하지 않아야 함