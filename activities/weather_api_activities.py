import asyncio

from temporalio import activity
from services.weather_api_service import WeatherApiService
from exceptions import InvalidLocationError
from shared import CurrentDetails, CurrentResponse
from activities import config


class WeatherApiActivities:
    def __init__(self):
        self.weather_api_service = WeatherApiService(
            host="api.weatherapi.com", api_key=config.get("WEATHER_API_KEY")
        )

    @activity.defn
    async def current(self, data: CurrentDetails) -> CurrentResponse:
        try:
            return await asyncio.to_thread(
                self.weather_api_service.get_current, location=data.location
            )
        except InvalidLocationError:
            raise
        except Exception:
            activity.logger.exception("Get current failed")
