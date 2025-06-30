from dataclasses import dataclass


WEATHER_API_CURRENT_QUEUE_NAME = "GET_CURRENT_OHIO_WEATHER"

@dataclass
class CurrentDetails:
    location: str


@dataclass
class CurrentResponse:
    name: str
    country: str
    text: str
    temp_c: float
    temp_f: float
