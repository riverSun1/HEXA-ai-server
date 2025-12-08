import uuid

from app.consult.application.port.consult_repository_port import ConsultRepositoryPort
from app.consult.application.port.ai_counselor_port import AICounselorPort
from app.consult.domain.consult_session import ConsultSession
from app.shared.vo.mbti import MBTI
from app.shared.vo.gender import Gender


class StartConsultUseCase:
    """상담 시작 유스케이스"""

    def __init__(self, repository: ConsultRepositoryPort, ai_counselor: AICounselorPort):
        self._repository = repository
        self._ai_counselor = ai_counselor

    def execute(self, user_id: str, mbti: MBTI, gender: Gender) -> dict:
        """
        상담을 시작한다.

        1. 세션 ID 생성
        2. ConsultSession 생성
        3. 세션 저장
        4. AI 인사말 생성
        5. 세션 ID와 인사말 반환
        """
        # 1. 세션 ID 생성
        session_id = str(uuid.uuid4())

        # 2. ConsultSession 생성
        session = ConsultSession(
            id=session_id,
            user_id=user_id,
            mbti=mbti,
            gender=gender
        )

        # 3. 세션 저장
        self._repository.save(session)

        # 4. AI 인사말 생성
        greeting = self._ai_counselor.generate_greeting(mbti, gender)

        # 5. 세션 ID와 인사말 반환
        return {"session_id": session_id, "greeting": greeting}
