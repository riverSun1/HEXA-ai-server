class Session:
    """세션 정보를 담는 도메인 객체"""

    def __init__(self, session_id: str, user_id: str):
        self._validate(session_id, user_id)
        self.session_id = session_id
        self.user_id = user_id

    def _validate(self, session_id: str, user_id: str) -> None:
        """Session 값의 유효성을 검증한다"""
        if not session_id:
            raise ValueError("session_id는 비어있을 수 없습니다")
        if not user_id:
            raise ValueError("user_id는 비어있을 수 없습니다")