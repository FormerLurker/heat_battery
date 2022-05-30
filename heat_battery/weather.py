from enum import Enum
import json
import requests
import settings

class WeatherServices(str, Enum):
    WEATHER_DOT_GOV: str = "weather.gov"


class Weather():
    def __init__(self):
        self.weather_dot_gov = WeatherDotGov()
        self._lat = 0
        self._lon = 0

    def set_location(self, lat, lon):
        self._lat = lat
        self._lon = lon

    def get_current_temperature(self, service, lat, lon, units):
        if service == WeatherServices.WEATHER_DOT_GOV:
            return self.weather_dot_gov.get_current_temperature(lat, lon, units)

        raise Weather.ServiceNotFoundException(
            f"The selected service is not found.  ServiceId: {self.weather_service}"
        )

    # Custom Exception Classes
    class ServiceNotFoundException(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)


class WeatherDotGov():
    def __init__(self):
        self.url_endpoint_base = "https://api.weather.gov"
        self.url_points = "points"

    def get_current_temperature(self, lat, lon, units):
        # create the request url

        points = self.get_points(lat, lon)
        forecast_hourly = self.get_forecast_hourly(points)
        properties = forecast_hourly["properties"]
        periods = properties["periods"]
        most_recent_period = periods[0]
        temp = most_recent_period["temperature"]
        temp_units = most_recent_period["temperatureUnit"]
        if temp_units == "F":
            return settings.UnitsConversion.ConvertTemp(settings.Units.IMPERIAL, temp, units)
        elif temp_units == "C":
            return settings.UnitsConversion.ConvertTemp(settings.Units.METRIC, temp, units)
        elif temp_units == "K":
            return settings.UnitsConversion.ConvertTemp(settings.Units.SCIENTIFIC, temp, units)
        else:
            raise UnsupportedUnitsException(f"Weather.gov returned units {units}, which is unsupported.")

    def get_points(self, lat, lon):
        url = f"{self.url_endpoint_base}/{self.url_points}/{lat},{lon}"
        # make the initial request
        resp = requests.get(url=url)
        data = resp.json()
        return data

    def get_forecast_hourly(self, points):
        properties = points["properties"]
        url = properties["forecastHourly"]
        resp = requests.get(url=url)
        data = resp.json()
        return data

class UnsupportedUnitsException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


