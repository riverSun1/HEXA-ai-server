from abc import ABC, abstractmethod

from app.auth.domain.session import Session


class SessionRepositoryPort(ABC):
    """세션 저장소 포트 인터페이스"""

    @abstractmethod
    def save(self, session: Session) -> None:
        """세션을 저장한다"""
        pass

    @abstractmethod
    def find_by_session_id(self, session_id: str) -> Session | None:
        """session_id로 세션을 조회한다"""
        pass

    @abstractmethod
    def delete(self, session_id: str) -> None:
        """세션을 삭제한다"""
        pass