import pytest
from unittest.mock import patch

from temporalio.testing import ActivityEnvironment

from weather_api_app.activities import WeatherApiActivities
from weather_api_app.shared import CurrentDetails
from weather_api_app.exceptions import InvalidLocationError


class TestWeatherApiActivities:

    def setup_method(self):
        self.activity_env = ActivityEnvironment()
        self.activity = WeatherApiActivities()

    @pytest.mark.asyncio
    async def test_current_success(self):
        data = CurrentDetails(location="London")
        result = await self.activity_env.run(self.activity.current, data)
        assert result.name == "London"

    @pytest.mark.asyncio
    async def test_invalid_location_exception(self):
        data = CurrentDetails(location=5)
        with pytest.raises(InvalidLocationError):
            await self.activity_env.run(self.activity.current, data)

    @pytest.mark.asyncio
    async def test_general_exception(self):
        data = CurrentDetails(location=5)
        with patch.object(
            self.activity.weather_api_service, "get_current", side_effect=Exception
        ):
            with pytest.raises(Exception):
                await self.activity_env.run(self.activity.current, data)
