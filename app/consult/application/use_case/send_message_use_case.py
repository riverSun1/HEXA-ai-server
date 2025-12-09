from app.consult.application.port.consult_repository_port import ConsultRepositoryPort
from app.consult.application.port.ai_counselor_port import AICounselorPort
from app.consult.domain.message import Message


class SendMessageUseCase:
    """메시지 전송 유스케이스"""

    def __init__(
        self,
        repository: ConsultRepositoryPort,
        ai_counselor: AICounselorPort
    ):
        self._repository = repository
        self._ai_counselor = ai_counselor

    def execute(self, session_id: str, user_id: str, content: str) -> dict:
        """
        메시지를 전송하고 AI 응답을 받는다.

        1. 세션 조회
        2. 세션 소유자 검증
        3. 세션 완료 여부 검증
        4. 사용자 메시지 저장
        5. AI 응답 생성
        6. AI 응답 저장
        7. 응답 반환
        """
        # 1. 세션 조회
        session = self._repository.find_by_id(session_id)
        if not session:
            raise ValueError("세션을 찾을 수 없습니다")

        # 2. 세션 소유자 검증
        if session.user_id != user_id:
            raise PermissionError("세션에 접근할 권한이 없습니다")

        # 3. 세션 완료 여부 검증
        if session.is_completed():
            raise ValueError("상담이 완료되었습니다")

        # 4. 사용자 메시지 저장
        user_message = Message(role="user", content=content)
        session.add_message(user_message)

        # 5. AI 응답 생성
        ai_response = self._ai_counselor.generate_response(session, content)

        # 6. AI 응답 저장
        assistant_message = Message(role="assistant", content=ai_response)
        session.add_message(assistant_message)

        # 7. 세션 저장 (업데이트)
        self._repository.save(session)

        # 8. 남은 턴 수 계산
        remaining_turns = max(0, 5 - session.get_user_turn_count())

        return {"response": ai_response, "remaining_turns": remaining_turns}
