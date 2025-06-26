from dotenv import load_dotenv
from dataclasses import dataclass
import asyncio
import os

from temporalio import activity
from weather_api_service import WeatherApiService
from exceptions import InvalidLocationError
from shared import CurrentDetails, CurrentResponse


load_dotenv(".env")
api_key = os.getenv("WEATHER_API_KEY")


class WeatherApiActivities:
    def __init__(self):
        print(f'api_key: {api_key}')
        self.weather_api_service = WeatherApiService(
            host="api.weatherapi.com",
            api_key=api_key
        )

    @activity.defn
    async def current(self, data: CurrentDetails) -> CurrentResponse:
        try:
            confirmation = await asyncio.to_thread(
                self.weather_api_service.get_current, location=data.location
            )
            print(f"{confirmation=}")
            return confirmation
        except InvalidLocationError:
            raise
        except Exception:
            activity.logger.exception("Get current failed")
