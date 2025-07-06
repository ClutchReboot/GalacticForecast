import pytest
from unittest.mock import patch

from temporalio.testing import ActivityEnvironment

from moon_phase_app.activities import MoonPhaseActivities
from moon_phase_app.shared import CityDetails
from moon_phase_app.exceptions import InvalidCityError


class TestMoonPhaseActivities:

    def setup_method(self):
        self.activity_env = ActivityEnvironment()
        self.activity = MoonPhaseActivities()

    @pytest.mark.asyncio
    async def test_city_success(self):
        data = CityDetails(
            city='Budapest'
        )
        result = await self.activity_env.run(self.activity.city, data)
        assert result.location == "Budapest"
        
    @pytest.mark.asyncio
    async def test_invalid_city_exception(self):
        data = CityDetails(
            city=5
        )
        with pytest.raises(InvalidCityError):
            await self.activity_env.run(self.activity.city, data)

    @pytest.mark.asyncio
    async def test_general_exception(self):
        data = CityDetails(
            city=5
        )
        with patch.object(self.activity.moon_phase_service, 'get_city', side_effect=Exception):
            with pytest.raises(Exception):
                await self.activity_env.run(self.activity.city, data)
