import datetime
import requests
from fastapi import HTTPException, status
from typing import List
from core.repository import AbstractRepository
from core.config import NBRB_API_URL
from schemas.rates import CurrencyRate, RateDirection, RateSchema


class RateService:
    def __init__(
        self, rates_repo: AbstractRepository, rate_imports_repo: AbstractRepository
    ):
        self.rates_repo: AbstractRepository = rates_repo()
        self.rate_imports_repo: AbstractRepository = rate_imports_repo()

    async def import_rates(self, date: datetime.date):
        rate_import = await self.rate_imports_repo.find_one_by_date(date)
        if rate_import:
            return

        try:
            nbrb_response = requests.get(f"{NBRB_API_URL}?ondate={date}&periodicity=0")
            data = [
                RateSchema(
                    currency_id=item["Cur_ID"],
                    value=item["Cur_OfficialRate"],
                    scale=item["Cur_Scale"],
                    date=date,
                ).dict()
                for item in nbrb_response.json()
            ]
            await self.rates_repo.import_rates(data)
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Error during import."},
            )

    async def get_rate(self, date: datetime.date, currency_id: int) -> CurrencyRate:
        previous_date = date - datetime.timedelta(days=1)
        rate_import = await self.rate_imports_repo.find_one_by_date(date)
        prev_rate_import = await self.rate_imports_repo.find_one_by_date(previous_date)

        if not rate_import:
            await self.import_rates(date)
        if not prev_rate_import:
            await self.import_rates(previous_date)

        requested_date = await self.rates_repo.find_one_by_id_from_date(
            date, currency_id
        )
        if not requested_date:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "No rate with such currency_id."},
            )
        prev = await self.rates_repo.find_one_by_id_from_date(
            previous_date, currency_id
        )

        direction = None
        if not prev:
            direction = RateDirection.NONE
        elif requested_date.value > prev.value:
            direction = RateDirection.UP
        elif requested_date.value < prev.value:
            direction = RateDirection.DOWN
        else:
            direction = RateDirection.SAME

        res = CurrencyRate(
            rate=requested_date,
            compared_with_previous=direction,
        )
        return res
