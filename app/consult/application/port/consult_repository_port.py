from abc import ABC, abstractmethod

from app.consult.domain.consult import ConsultHistory


class ConsultRepositoryPort(ABC):
    @abstractmethod
    def save(self, consult: ConsultHistory) -> ConsultHistory:
        raise NotImplementedError
