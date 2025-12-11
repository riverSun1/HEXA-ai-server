from datetime import datetime, timedelta

from sqlalchemy.orm import Session as DbSession

from app.auth.application.port.session_repository_port import SessionRepositoryPort
from app.auth.domain.session import Session
from app.user.infrastructure.model.user_model import UserModel


class MySqlSessionRepository(SessionRepositoryPort):
    """MySQL 기반 세션 저장소 (User 테이블 사용)"""

    DEFAULT_TTL_SECONDS = 60 * 60 * 6  # 6시간

    def __init__(self, db_session: DbSession, ttl_seconds: int | None = None):
        self._db = db_session
        self._ttl = ttl_seconds if ttl_seconds is not None else self.DEFAULT_TTL_SECONDS

    def save(self, session: Session) -> None:
        """세션을 저장한다"""
        user = self._db.query(UserModel).filter(
            UserModel.id == session.user_id
        ).first()

        if user:
            user.session_id = session.session_id
            user.session_expires_at = datetime.now() + timedelta(seconds=self._ttl)
            self._db.commit()

    def find_by_session_id(self, session_id: str) -> Session | None:
        """session_id로 세션을 조회한다"""
        user = self._db.query(UserModel).filter(
            UserModel.session_id == session_id
        ).first()

        if user is None:
            return None

        # 만료 체크
        if user.session_expires_at and user.session_expires_at < datetime.now():
            self.delete(session_id)
            return None

        return Session(
            session_id=user.session_id,
            user_id=user.id,
        )

    def delete(self, session_id: str) -> None:
        """세션을 삭제한다"""
        user = self._db.query(UserModel).filter(
            UserModel.session_id == session_id
        ).first()

        if user:
            user.session_id = None
            user.session_expires_at = None
            self._db.commit()