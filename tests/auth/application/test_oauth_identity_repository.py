import pytest
from app.auth.domain.oauth_identity import OAuthIdentity
from app.auth.infrastructure.repository.in_memory_oauth_identity_repository import (
    InMemoryOAuthIdentityRepository,
)


def test_save_and_find_oauth_identity():
    """OAuthIdentity를 저장하고 provider/provider_user_id로 조회할 수 있다"""
    # Given: 저장소와 OAuthIdentity
    repository = InMemoryOAuthIdentityRepository()
    identity = OAuthIdentity(
        provider="google",
        provider_user_id="google-123",
        email="test@gmail.com"
    )

    # When: 저장하고 조회하면
    repository.save(identity)
    found = repository.find_by_provider_and_provider_user_id("google", "google-123")

    # Then: 동일한 OAuthIdentity를 반환한다
    assert found is not None
    assert found.provider == "google"
    assert found.provider_user_id == "google-123"
    assert found.email == "test@gmail.com"


def test_find_nonexistent_oauth_identity_returns_none():
    """존재하지 않는 provider/provider_user_id로 조회하면 None을 반환한다"""
    # Given: 빈 저장소
    repository = InMemoryOAuthIdentityRepository()

    # When: 존재하지 않는 identity를 조회하면
    found = repository.find_by_provider_and_provider_user_id("google", "nonexistent")

    # Then: None을 반환한다
    assert found is None


def test_find_different_provider_returns_none():
    """같은 provider_user_id라도 다른 provider면 None을 반환한다"""
    # Given: google provider로 저장된 identity
    repository = InMemoryOAuthIdentityRepository()
    identity = OAuthIdentity(
        provider="google",
        provider_user_id="user-123",
        email="test@gmail.com"
    )
    repository.save(identity)

    # When: kakao provider로 조회하면
    found = repository.find_by_provider_and_provider_user_id("kakao", "user-123")

    # Then: None을 반환한다
    assert found is None