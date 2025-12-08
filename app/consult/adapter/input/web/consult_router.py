from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

from app.consult.application.use_case.start_consult_use_case import StartConsultUseCase
from app.consult.application.use_case.send_message_use_case import SendMessageUseCase
from app.user.application.port.user_repository_port import UserRepositoryPort
from app.consult.application.port.consult_repository_port import ConsultRepositoryPort
from app.consult.application.port.ai_counselor_port import AICounselorPort
from app.auth.adapter.input.web.auth_dependency import get_current_user_id

consult_router = APIRouter()

# Global repository instances (will be injected in tests)
_user_repository: UserRepositoryPort | None = None
_consult_repository: ConsultRepositoryPort | None = None
_ai_counselor: AICounselorPort | None = None


class SendMessageRequest(BaseModel):
    content: str


@consult_router.post("/start")
def start_consult(user_id: str = Depends(get_current_user_id)):
    """
    상담 세션을 시작한다.

    1. user_id로 User 조회
    2. User의 MBTI, Gender 확인
    3. StartConsultUseCase 실행
    4. 세션 ID 반환
    """
    # User 조회
    if not _user_repository:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User repository가 설정되지 않았습니다",
        )

    user = _user_repository.find_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다",
        )

    # MBTI, Gender 확인
    if not user.mbti or not user.gender:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="프로필 정보(MBTI, 성별)를 먼저 입력해주세요",
        )

    # Use case 실행
    if not _consult_repository:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Consult repository가 설정되지 않았습니다",
        )

    if not _ai_counselor:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI counselor가 설정되지 않았습니다",
        )

    use_case = StartConsultUseCase(_consult_repository, _ai_counselor)
    result = use_case.execute(user_id=user_id, mbti=user.mbti, gender=user.gender)

    return result


@consult_router.post("/{session_id}/message")
def send_message(
    session_id: str,
    request: SendMessageRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    메시지를 전송하고 AI 응답을 받는다.

    1. 세션 조회 및 소유자 검증
    2. 메시지 전송
    3. AI 응답 반환
    """
    if not _consult_repository:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Consult repository가 설정되지 않았습니다",
        )

    if not _ai_counselor:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI counselor가 설정되지 않았습니다",
        )

    use_case = SendMessageUseCase(_consult_repository, _ai_counselor)

    try:
        result = use_case.execute(
            session_id=session_id,
            user_id=user_id,
            content=request.content
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
