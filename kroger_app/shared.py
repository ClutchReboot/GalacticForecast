from dataclasses import dataclass


KROGER_QUEUE_NAME = "GET_CITY_BUDAPEST_MOON_PHASE"


@dataclass
class CityDetails:
    city: str


@dataclass
class CityResponse:
    @dataclass
    class Moon:
        phase: str
        info: str
        visible: str
        altitude: str
        distance: str
        next_full_moon: str
        next_new_moon: str
        today_moonrise: str
        today_moonset: str
        img_flat: str

        @classmethod
        def from_dict(cls, data: dict) -> "CityResponse.Moon":
            return cls(
                phase=data.get("phase", None),
                info=data.get("info", None),
                visible=data.get("visible", None),
                altitude=data.get("altitude", None),
                distance=data.get("distance", None),
                next_full_moon=data.get("next_full_moon", None),
                next_new_moon=data.get("next_new_moon", None),
                today_moonrise=data.get("today_moonrise", None),
                today_moonset=data.get("today_moonset", None),
                img_flat=data.get("img_flat", None),
            )

    moon: Moon
    location: str
    today: str
    last_update: float
    supported: float

    @classmethod
    def from_dict(cls, data: dict) -> "CityResponse":
        moon_data = CityResponse.Moon.from_dict(data.get("moon", {}))
        return cls(
            moon=moon_data,
            location=data.get("location", None),
            today=data.get("today", None),
            last_update=data.get("last_update", None),
            supported=data.get("supported", None),
        )
