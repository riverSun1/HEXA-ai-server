from app.auth.application.port.session_repository_port import SessionRepositoryPort
from app.auth.domain.session import Session


class InMemorySessionRepository(SessionRepositoryPort):
    """인메모리 세션 저장소 (테스트용)"""

    def __init__(self):
        self._sessions: dict[str, Session] = {}

    def save(self, session: Session) -> None:
        """세션을 저장한다"""
        self._sessions[session.session_id] = session

    def find_by_session_id(self, session_id: str) -> Session | None:
        """session_id로 세션을 조회한다"""
        return self._sessions.get(session_id)

    def delete(self, session_id: str) -> None:
        """세션을 삭제한다"""
        self._sessions.pop(session_id, None)