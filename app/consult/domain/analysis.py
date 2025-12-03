from typing import List

from pydantic import BaseModel, Field


class ConcernAnalysis(BaseModel):
    """분석 에이전트 결과"""

    summary: str = Field(..., description="고민 한 줄 요약")
    category: str = Field(..., description="고민 카테고리")
    user_role: str = Field(..., description="사용자 역할")
    counterparty: str = Field(..., description="상대방 유형")
    emotion: List[str] = Field(default_factory=list, description="감정 목록")
    urgency: int = Field(..., description="긴급도(1~5)")
    main_question: str = Field(..., description="핵심 질문")
    constraints: List[str] = Field(default_factory=list, description="제약사항")
    keywords: List[str] = Field(default_factory=list, description="키워드")
    suicide_risk: bool = Field(..., description="자살 위험 여부")
