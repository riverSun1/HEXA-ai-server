from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from openai import AsyncOpenAI

from app.consult.adapter.input.web.request.consult_request import ConsultRequest
from app.consult.adapter.input.web.response.consult_response import ConsultResponse
from app.consult.application.use_case.consult_use_case import ConsultUseCase
from app.consult.infrastructure.repository.consult_repository_impl import ConsultRepositoryImpl
from app.consult.infrastructure.service.openai_service import (
    OpenAICounselingService,
    OpenAINlpAnalysisService,
)
from config.database.session import get_db
from config.settings import get_settings

consult_router = APIRouter()


async def get_consult_use_case(db: Session = Depends(get_db)) -> ConsultUseCase:
    settings = get_settings()
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    model = "gpt-4o-mini"

    analysis_service = OpenAINlpAnalysisService(client=client, model=model)
    counseling_service = OpenAICounselingService(client=client, model=model)
    repository = ConsultRepositoryImpl(db_session=db)

    return ConsultUseCase(
        analysis_port=analysis_service,
        counseling_port=counseling_service,
        consult_repository=repository,
    )


@consult_router.post("/consult", response_model=ConsultResponse)
async def consult(
    request: ConsultRequest,
    use_case: ConsultUseCase = Depends(get_consult_use_case),
) -> ConsultResponse:
    result = await use_case.execute(text=request.text, user_id=request.user_id)
    return ConsultResponse(analysis=result.analysis, answer=result.answer)
