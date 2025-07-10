import asyncio

from temporalio import activity
from weather_api_app.service import WeatherApiService
from weather_api_app.exceptions import InvalidLocationError
from weather_api_app.shared import CurrentDetails, CurrentResponse
from weather_api_app import config


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
            raise
