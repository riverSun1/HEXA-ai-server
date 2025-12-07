from abc import ABC, abstractmethod

from app.user.domain.user import User


class UserRepositoryPort(ABC):
    """유저 저장소 포트 인터페이스"""

    @abstractmethod
    def save(self, user: User) -> None:
        """유저를 저장한다"""
        pass

    @abstractmethod
    def find_by_id(self, user_id: str) -> User | None:
        """id로 유저를 조회한다"""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        """email로 유저를 조회한다"""
        pass