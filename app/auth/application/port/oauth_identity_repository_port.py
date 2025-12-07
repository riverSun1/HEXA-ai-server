from abc import ABC, abstractmethod

from app.auth.domain.oauth_identity import OAuthIdentity


class OAuthIdentityRepositoryPort(ABC):
    """OAuthIdentity 저장소 포트 인터페이스"""

    @abstractmethod
    def save(self, identity: OAuthIdentity) -> None:
        """OAuthIdentity를 저장한다"""
        pass

    @abstractmethod
    def find_by_provider_and_provider_user_id(
        self, provider: str, provider_user_id: str
    ) -> OAuthIdentity | None:
        """provider와 provider_user_id로 OAuthIdentity를 조회한다"""
        pass