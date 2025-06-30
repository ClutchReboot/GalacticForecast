import requests

from exceptions import InvalidLocationError, RequestError
from shared import CurrentResponse


class WeatherApiService:
    def __init__(self, host: str, api_key: str):
        """
        Swagger: https://app.swaggerhub.com/apis-docs/WeatherAPI.com/WeatherAPI/1.0.2#/
        """
        self.host = host
        self.api_key = api_key

    def get_current(self, location: str) -> requests:
        try:
            if not isinstance(location, str):
                raise InvalidLocationError(
                    'Invalid Type. Location should be of type "string".'
                )

            url = f"http://{self.host}/v1/current.json?key={self.api_key}&q={location}&aqi=no"
            r = requests.get(url, headers={"Content-Type": "application/json"})

            if not r.ok:
                raise RequestError("Failed to get 200 from endpoint.")

            data = r.json()
            result: CurrentResponse = CurrentResponse(
                name=data.get("location", {}).get("name", None),
                country=data.get("location", {}).get("country", None),
                text=data.get("current", {}).get("condition", {}).get("text", None),
                temp_c=data.get("current", {}).get("temp_c", None),
                temp_f=data.get("current", {}).get("temp_f", None),
            )
            return result
        except Exception:
            raise
