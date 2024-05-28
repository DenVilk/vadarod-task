import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, insert, and_
from models import Rate, RateImport
from core.repository import SQLAlchemyRepository
from core.database import async_session_maker


class RateRepository(SQLAlchemyRepository):
    model = Rate

    async def import_rates(self, data: List[Dict[str, Any]]) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(data).returning(self.model.id)
            await session.execute(stmt)
            stmt_import = (
                insert(RateImport)
                .values({"date": data[0]["date"]})
                .returning(RateImport.id)
            )
            await session.execute(stmt_import)
            await session.commit()

    async def find_one_by_id_from_date(
        self,
        date: datetime.date,
        currency_id: int,
    ) -> Rate:
        async with async_session_maker() as session:
            stmt = select(self.model).where(
                and_(
                    self.model.date == date,
                    self.model.currency_id == currency_id,
                )
            )
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            if not res:
                return None
            return res[0]


class RateImportRepository(SQLAlchemyRepository):
    model = RateImport

    async def find_one_by_date(self, date: datetime.date) -> Optional[RateImport]:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.date == date)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            if not res:
                return None
            return res[0]
