import datetime
from sqlalchemy import Column, Date, DateTime, Float, Integer
from schemas.rates import RateImportSchema, RateSchema
from core.database import Base


class Rate(Base):
    __tablename__ = "rates"

    id = Column(Integer, primary_key=True)
    currency_id = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)
    scale = Column(Integer, nullable=False)
    date = Column(Date(), default=datetime.datetime.now)

    def to_read_model(self) -> RateSchema:
        return RateSchema(
            currency_id=self.currency_id,
            value=self.value,
            scale=self.scale,
            date=self.date,
        )


class RateImport(Base):
    __tablename__ = "rate_imports"

    id = Column(Integer, primary_key=True)
    date = Column(Date(), nullable=False)

    def to_read_model(self) -> RateImportSchema:
        return RateImportSchema(
            id=self.id,
            date=self.date,
        )
