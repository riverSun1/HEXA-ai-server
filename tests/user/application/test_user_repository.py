import pytest
from app.user.domain.user import User
from app.user.infrastructure.repository.in_memory_user_repository import (
    InMemoryUserRepository,
)


def test_save_and_find_user_by_id():
    """유저를 저장하고 id로 조회할 수 있다"""
    # Given: 저장소와 유저
    repository = InMemoryUserRepository()
    user = User(id="user-123", email="test@example.com")

    # When: 유저를 저장하고 조회하면
    repository.save(user)
    found = repository.find_by_id("user-123")

    # Then: 동일한 유저를 반환한다
    assert found is not None
    assert found.id == "user-123"
    assert found.email == "test@example.com"


def test_find_nonexistent_user_returns_none():
    """존재하지 않는 id로 조회하면 None을 반환한다"""
    # Given: 빈 저장소
    repository = InMemoryUserRepository()

    # When: 존재하지 않는 유저를 조회하면
    found = repository.find_by_id("nonexistent")

    # Then: None을 반환한다
    assert found is None


def test_find_user_by_email():
    """email로 유저를 조회할 수 있다"""
    # Given: 저장된 유저
    repository = InMemoryUserRepository()
    user = User(id="user-123", email="test@example.com")
    repository.save(user)

    # When: email로 조회하면
    found = repository.find_by_email("test@example.com")

    # Then: 동일한 유저를 반환한다
    assert found is not None
    assert found.id == "user-123"


def test_find_nonexistent_email_returns_none():
    """존재하지 않는 email로 조회하면 None을 반환한다"""
    # Given: 빈 저장소
    repository = InMemoryUserRepository()

    # When: 존재하지 않는 email로 조회하면
    found = repository.find_by_email("nonexistent@example.com")

    # Then: None을 반환한다
    assert found is None