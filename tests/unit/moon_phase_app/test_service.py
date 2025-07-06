import pytest
from unittest.mock import Mock, patch

from moon_phase_app.service import MoonPhaseService
from moon_phase_app.shared import CityResponse
from moon_phase_app.exceptions import RequestError, InvalidCityError
from moon_phase_app import config

api_key = config.get("MOON_PHASE_API_KEY")


class TestGetCurrent:
    def test_returned_result(self):
        mps = MoonPhaseService(host="moon-phase1.p.rapidapi.com", api_key=api_key)
        results: CityResponse = mps.get_city(city="budapest")
        assert type(results) == CityResponse
        assert results.location == "Budapest"

    def test_invalid_location_exception(self):
        mps = MoonPhaseService(host="moon-phase1.p.rapidapi.com", api_key=api_key)
        with pytest.raises(InvalidCityError):
            mps.get_city(city=5)

    def test_request_exception(self):
        mock_response = Mock()
        mock_response.ok = False  # Simulate failed request
        mock_response.status_code = 500

        mps = MoonPhaseService(host="moon-phase1.p.rapidapi.com", api_key=api_key)
        with patch("requests.get", return_value=mock_response):
            with pytest.raises(RequestError):
                mps.get_city(city="Budapest")
