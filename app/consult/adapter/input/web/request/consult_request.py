from typing import Optional

from pydantic import BaseModel, Field


class ConsultRequest(BaseModel):
    text: str = Field(..., description="사용자 고민 텍스트")
    user_id: Optional[int] = Field(None, description="사용자 ID")
