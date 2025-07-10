import requests

from moon_phase_app.exceptions import InvalidCityError, RequestError
from moon_phase_app.shared import CityResponse


class MoonPhaseService:
    def __init__(self, host: str, api_key: str):
        """
        RapidAPI: https://rapidapi.com/thestevepappa/api/moon-phase1
        """
        self.host = host
        self.api_key = api_key

        self.headers = {"x-rapidapi-host": self.host, "x-rapidapi-key": self.api_key}

    def get_city(self, city: str) -> CityResponse:
        try:
            if not isinstance(city, str):
                raise InvalidCityError(
                    'Invalid Type. Location should be of type "string".'
                )

            url = f"https://{self.host}/?city={city}"
            r = requests.get(url, headers=self.headers)

            if not r.ok:
                raise RequestError("Failed to get 200 from endpoint.")

            return CityResponse.from_dict(data=r.json())
        except Exception:
            raise
