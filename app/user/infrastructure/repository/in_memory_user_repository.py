from app.user.application.port.user_repository_port import UserRepositoryPort
from app.user.domain.user import User


class InMemoryUserRepository(UserRepositoryPort):
    """인메모리 유저 저장소 (테스트용)"""

    def __init__(self):
        self._users: dict[str, User] = {}

    def save(self, user: User) -> None:
        """유저를 저장한다"""
        self._users[user.id] = user

    def find_by_id(self, user_id: str) -> User | None:
        """id로 유저를 조회한다"""
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> User | None:
        """email로 유저를 조회한다"""
        for user in self._users.values():
            if user.email == email:
                return user
        return None