import pytest

from app.consult.domain.consult_session import ConsultSession
from app.consult.application.use_case.send_message_use_case import SendMessageUseCase
from app.shared.vo.mbti import MBTI
from app.shared.vo.gender import Gender
from tests.consult.fixtures.fake_consult_repository import FakeConsultRepository
from tests.consult.fixtures.fake_ai_counselor import FakeAICounselor


class TestSendMessageUseCase:
    """SendMessageUseCase 테스트"""

    def setup_method(self):
        self.repository = FakeConsultRepository()
        self.ai_counselor = FakeAICounselor(response="AI 응답입니다")
        self.use_case = SendMessageUseCase(self.repository, self.ai_counselor)

        # 테스트용 세션 생성
        self.session = ConsultSession(
            id="session-123",
            user_id="user-456",
            mbti=MBTI("INTJ"),
            gender=Gender("MALE")
        )
        self.repository.save(self.session)

    def test_send_message_returns_ai_response(self):
        """메시지 전송 시 AI 응답을 반환한다"""
        # When
        result = self.use_case.execute(
            session_id="session-123",
            user_id="user-456",
            content="안녕하세요"
        )

        # Then
        assert result["response"] == "AI 응답입니다"

    def test_send_message_saves_user_message(self):
        """사용자 메시지가 세션에 저장된다"""
        # When
        self.use_case.execute(
            session_id="session-123",
            user_id="user-456",
            content="안녕하세요"
        )

        # Then
        session = self.repository.find_by_id("session-123")
        messages = session.get_messages()
        user_messages = [m for m in messages if m.role == "user"]
        assert len(user_messages) == 1
        assert user_messages[0].content == "안녕하세요"

    def test_send_message_saves_ai_response(self):
        """AI 응답이 세션에 저장된다"""
        # When
        self.use_case.execute(
            session_id="session-123",
            user_id="user-456",
            content="안녕하세요"
        )

        # Then
        session = self.repository.find_by_id("session-123")
        messages = session.get_messages()
        assistant_messages = [m for m in messages if m.role == "assistant"]
        assert len(assistant_messages) == 1
        assert assistant_messages[0].content == "AI 응답입니다"

    def test_send_message_rejects_non_owner(self):
        """세션 소유자가 아니면 에러를 발생시킨다"""
        # When & Then
        with pytest.raises(PermissionError, match="세션에 접근할 권한이 없습니다"):
            self.use_case.execute(
                session_id="session-123",
                user_id="other-user",
                content="안녕하세요"
            )

    def test_send_message_rejects_nonexistent_session(self):
        """존재하지 않는 세션이면 에러를 발생시킨다"""
        # When & Then
        with pytest.raises(ValueError, match="세션을 찾을 수 없습니다"):
            self.use_case.execute(
                session_id="nonexistent",
                user_id="user-456",
                content="안녕하세요"
            )

    def test_send_message_rejects_when_session_completed(self):
        """5턴 완료된 세션에 메시지를 보내면 에러를 발생시킨다"""
        from app.consult.domain.message import Message

        # Given: 5턴 완료된 세션
        for i in range(5):
            self.session.add_message(Message(role="user", content=f"질문 {i+1}"))
            self.session.add_message(Message(role="assistant", content=f"답변 {i+1}"))
        self.repository.save(self.session)

        # When & Then: 6번째 메시지 전송 시 에러
        with pytest.raises(ValueError, match="상담이 완료되었습니다"):
            self.use_case.execute(
                session_id="session-123",
                user_id="user-456",
                content="추가 질문"
            )