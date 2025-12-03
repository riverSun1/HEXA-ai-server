import json
from sqlalchemy.orm import Session

from app.consult.application.port.consult_repository_port import ConsultRepositoryPort
from app.consult.domain.analysis import ConcernAnalysis
from app.consult.domain.consult import ConsultHistory
from app.consult.infrastructure.orm.consult_orm import ConsultORM


class ConsultRepositoryImpl(ConsultRepositoryPort):
    def __init__(self, db_session: Session):
        self.db = db_session

    def save(self, consult: ConsultHistory) -> ConsultHistory:
        analysis_json = consult.analysis.model_dump_json(ensure_ascii=False)
        orm_obj = ConsultORM(
            user_id=consult.user_id,
            original_text=consult.original_text,
            analysis_json=analysis_json,
            answer=consult.answer,
            created_at=consult.created_at,
        )
        self.db.add(orm_obj)
        self.db.flush()

        consult.id = orm_obj.id
        return consult

    @staticmethod
    def to_domain(row: ConsultORM) -> ConsultHistory:
        analysis_dict = json.loads(row.analysis_json)
        analysis = ConcernAnalysis(**analysis_dict)
        history = ConsultHistory(
            user_id=row.user_id,
            original_text=row.original_text,
            analysis=analysis,
            answer=row.answer,
            created_at=row.created_at,
        )
        history.id = row.id
        return history
