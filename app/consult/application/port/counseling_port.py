from abc import ABC, abstractmethod

from app.consult.domain.analysis import ConcernAnalysis


class CounselingPort(ABC):
    @abstractmethod
    async def generate(self, text: str, analysis: ConcernAnalysis) -> str:
        raise NotImplementedError
