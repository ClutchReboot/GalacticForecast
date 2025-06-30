import pytest
from unittest.mock import Mock, patch

from weather_api_app.service import WeatherApiService
from weather_api_app.shared import CurrentResponse
from weather_api_app.exceptions import RequestError, InvalidLocationError
from weather_api_app import config

api_key = config.get("WEATHER_API_KEY")


class TestGetCurrent:
    def test_returned_result(self):
        was = WeatherApiService(host="api.weatherapi.com", api_key=api_key)
        results: CurrentResponse = was.get_current("London")
        assert type(results) == CurrentResponse
        assert results.name == "London"

    def test_invalid_location_exception(self):
        was = WeatherApiService(host="api.weatherapi.com", api_key=api_key)
        with pytest.raises(InvalidLocationError):
            was.get_current(location=5)

    def test_request_exception(self):
        mock_response = Mock()
        mock_response.ok = False  # Simulate failed request
        mock_response.status_code = 500

        was = WeatherApiService(host="api.weatherapi.com", api_key=api_key)
        with patch("requests.get", return_value=mock_response):
            with pytest.raises(RequestError):
                was.get_current(location="London")
