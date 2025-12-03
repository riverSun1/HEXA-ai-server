from abc import ABC, abstractmethod

from app.consult.domain.analysis import ConcernAnalysis


class NlpAnalysisPort(ABC):
    @abstractmethod
    async def analyze(self, text: str) -> ConcernAnalysis:
        raise NotImplementedError
