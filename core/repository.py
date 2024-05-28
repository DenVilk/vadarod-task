from abc import ABC, abstractmethod

from sqlalchemy import insert, select

from core.database import async_session_maker
from core import exceptions


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_all(self):
        async with async_session_maker() as session:
            stmt = select(self.model).order_by(self.model.created_at.desc())
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res

    async def find_one_by_id(self, id):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            if not res:
                raise exceptions.NOT_FOUND
            return res[0]