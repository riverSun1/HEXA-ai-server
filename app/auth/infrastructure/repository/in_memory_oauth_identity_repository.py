from app.auth.application.port.oauth_identity_repository_port import (
    OAuthIdentityRepositoryPort,
)
from app.auth.domain.oauth_identity import OAuthIdentity


class InMemoryOAuthIdentityRepository(OAuthIdentityRepositoryPort):
    """인메모리 OAuthIdentity 저장소 (테스트용)"""

    def __init__(self):
        self._identities: dict[str, OAuthIdentity] = {}

    def _make_key(self, provider: str, provider_user_id: str) -> str:
        """provider와 provider_user_id로 유니크한 키를 생성한다"""
        return f"{provider}:{provider_user_id}"

    def save(self, identity: OAuthIdentity) -> None:
        """OAuthIdentity를 저장한다"""
        key = self._make_key(identity.provider, identity.provider_user_id)
        self._identities[key] = identity

    def find_by_provider_and_provider_user_id(
        self, provider: str, provider_user_id: str
    ) -> OAuthIdentity | None:
        """provider와 provider_user_id로 OAuthIdentity를 조회한다"""
        key = self._make_key(provider, provider_user_id)
        return self._identities.get(key)