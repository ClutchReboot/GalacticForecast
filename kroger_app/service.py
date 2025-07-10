import requests

from kroger_app.exceptions import RequestError
from kroger_app.shared import CityResponse


class KrogerService:
    def __init__(self, host: str, api_key: str):
        """
        RapidAPI: https://developer.kroger.com/api-products/api/product-api-public
        """
        self.host = host if host else "api.kroger.com"
        self.api_key = api_key

        self.headers = {
            "accept": "application/json",
            "x-rapidapi-host": self.host,
            "x-rapidapi-key": self.api_key,
        }

    def get_city(self, term: str, location_id: int) -> CityResponse:
        try:
            if all(
                [
                    not isinstance(term, str),
                    not isinstance(location_id, int),
                ]
            ):
                raise TypeError('Invalid Type. Location should be of type "string".')

            url = f"https://{self.host}/v1/products?filter.term={term}&filter.locationId={location_id}"
            r = requests.get(url, headers=self.headers)

            if not r.ok:
                raise requests.RequestException("Failed to get 200 from endpoint.")

            return CityResponse.from_dict(data=r.json())
        except Exception:
            raise
