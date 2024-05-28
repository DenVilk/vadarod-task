import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.rates import CurrencyRate, RateSchema
from services.rates import RateService
from core.dependencies import rates_service

router = APIRouter(
    prefix="/rates",
)


@router.get("/")
async def import_rates(
    date: datetime.date,
    rates_service: RateService = Depends(rates_service),
):
    '''
    Method import rates for all currencies for [date].
    '''
    if date > datetime.date.today():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "You can't import rates for future dates."})
    await rates_service.import_rates(date)
    return {"message": "Rates were successfully imported."}


@router.get("/{currency_id:int}/")
async def get_rate(
    date: datetime.date,
    currency_id: int,
    rates_service: RateService = Depends(rates_service),
)->CurrencyRate:
    '''
    Method get rates for [date], for currency with [currency_id].
    If rates for [date] don't exist, it will import them.
    If currency with [currency_id] doesn't exist, it will give 404.
    '''
    rate = await rates_service.get_rate(date, currency_id)
    return rate
