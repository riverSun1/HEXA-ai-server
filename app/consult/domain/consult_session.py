from datetime import datetime
from app.shared.vo.mbti import MBTI
from app.shared.vo.gender import Gender
from app.consult.domain.message import Message


class ConsultSession:
    """상담 세션 도메인 엔티티"""

    def __init__(
        self,
        id: str,
        user_id: str,
        mbti: MBTI,
        gender: Gender,
        created_at: datetime | None = None,
    ):
        self._validate(id, user_id, mbti, gender)
        self.id = id
        self.user_id = user_id
        self.mbti = mbti
        self.gender = gender
        self.created_at = created_at or datetime.now()
        self._messages: list[Message] = []

    def _validate(self, id: str, user_id: str, mbti: MBTI | None, gender: Gender | None) -> None:
        """ConsultSession 값의 유효성을 검증한다"""
        if not id:
            raise ValueError("ConsultSession id는 비어있을 수 없습니다")
        if not user_id:
            raise ValueError("ConsultSession user_id는 비어있을 수 없습니다")
        if mbti is None:
            raise ValueError("ConsultSession mbti는 None일 수 없습니다")
        if gender is None:
            raise ValueError("ConsultSession gender는 None일 수 없습니다")

    def add_message(self, message: Message) -> None:
        """세션에 메시지를 추가한다"""
        self._messages.append(message)

    def get_messages(self) -> list[Message]:
        """세션의 모든 메시지를 반환한다"""
        return list(self._messages)

    def get_user_turn_count(self) -> int:
        """유저 메시지(턴) 개수를 반환한다"""
        return sum(1 for msg in self._messages if msg.role == "user")

    def is_completed(self) -> bool:
        """세션이 완료되었는지 (5턴 이상) 반환한다"""
        return self.get_user_turn_count() >= 5
