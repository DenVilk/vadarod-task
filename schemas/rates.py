import datetime
import enum
from typing import Optional
from pydantic import BaseModel

class RateDirection(enum.Enum):
    UP = "Up"
    DOWN = "Down"
    SAME = 'Same'
    NONE = "No rate for this date."

class RateSchema(BaseModel):
    currency_id: int
    value: float
    scale: int
    date: Optional[datetime.date]


class RateImportSchema(BaseModel):
    id: int
    date: Optional[datetime.date]


class CurrencyRate(BaseModel):
    rate: RateSchema
    compared_with_previous: RateDirection