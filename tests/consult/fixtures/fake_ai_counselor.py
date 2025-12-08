from app.consult.application.port.ai_counselor_port import AICounselorPort
from app.shared.vo.mbti import MBTI
from app.shared.vo.gender import Gender


class FakeAICounselor(AICounselorPort):
    """테스트용 Fake AI Counselor"""

    def generate_greeting(self, mbti: MBTI, gender: Gender) -> str:
        """간단한 고정 인사말을 반환한다"""
        return f"안녕하세요! {mbti.value} 유형이시군요. 어떤 관계 고민이 있으세요?"
from app.consult.domain.consult_session import ConsultSession


class FakeAICounselor(AICounselorPort):
    """테스트용 Fake AI 상담사"""

    def __init__(self, response: str = "AI 응답입니다"):
        self._response = response

    def generate_response(self, session: ConsultSession, user_message: str) -> str:
        return self._response

    def set_response(self, response: str) -> None:
        """테스트용: 응답 설정"""
        self._response = response
