from repository.rates import RateImportRepository, RateRepository
from services.rates import RateService


def rates_service() -> RateService:
    return RateService(RateRepository, RateImportRepository)
