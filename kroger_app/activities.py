import asyncio

from temporalio import activity

from kroger_app.service import MoonPhaseService
from kroger_app.exceptions import InvalidCityError
from kroger_app.shared import CityDetails, CityResponse
from kroger_app import config


class MoonPhaseActivities:
    def __init__(self):
        self.moon_phase_service = MoonPhaseService(
            host="moon-phase1.p.rapidapi.com", api_key=config.get("MOON_PHASE_API_KEY")
        )

    @activity.defn
    async def city(self, data: CityDetails) -> CityResponse:
        try:
            return await asyncio.to_thread(
                self.moon_phase_service.get_city, city=data.city
            )
        except InvalidCityError:
            raise
        except Exception:
            activity.logger.exception("Get current failed")
            raise
