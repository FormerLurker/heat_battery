from enum import Enum
from weather import WeatherServices
import os
import json

class Units(str, Enum):
    IMPERIAL: str = "imperial"
    METRIC: str = "metric"
    SCIENTIFIC: str = "scientific"

class UnitsConversion():
    @staticmethod
    def ConvertTemp(base_unit, temp, target_unit):
        if base_unit == Units.IMPERIAL:
            if target_unit == Units.METRIC:
                return (temp-32) * (5.0/9.0)
            if target_unit == Units.SCIENTIFIC:
                return (temp - 32) * (5.0 / 9.0) + 273.15
        if base_unit == Units.METRIC:
            if target_unit == Units.IMPERIAL:
                return (temp * 9.0/5.0) + 32
            if target_unit == Units.SCIENTIFIC:
                return temp + 273.15
        if base_unit == Units.SCIENTIFIC:
            if target_unit == Units.IMPERIAL:
                return (temp - 273.15) * (9.0/5.0) + 32
            if target_unit == Units.METRIC:
                return temp - 273.15
        return temp

class Settings():
    def __init__(self, settings_path):
        self.temperature_units = Units.METRIC
        self.temperature_variance = 2
        self.temperature_target = 23.0
        self.refresh_interval_ms = 5000
        self.weather_service = WeatherServices.WEATHER_DOT_GOV
        self.lat = 39.7456
        self.lon = -97.0892
        self._settings_path = settings_path

    def load(self):
        if not os.path.exists(self._settings_path):
            self.save()

        with open(self._settings_path, "r") as settings_file:
            settings_dict = json.load(settings_file)
            self.update_from_dict(settings_dict)

    def save(self):
        directory_path = os.path.dirname(self._settings_path)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        settings_dict = self.to_dict()
        with open(self._settings_path, "w+") as settings_file:
            json.dump(settings_dict, settings_file, indent=6)

    def to_dict(self):
        settings_dict = {
            "temperature_units": self.temperature_units,
            "temperature_variance": self.temperature_variance,
            "temperature_target": self.temperature_target,
            "refresh_interval_ms": self.refresh_interval_ms,
            "weather_service": self.weather_service,
            "lat": self.lat,
            "lon": self.lon
        }
        return settings_dict

    def update_from_dict(self, settings_dict):
        self.temperature_units = settings_dict["temperature_units"]
        self.temperature_variance = settings_dict["temperature_variance"]
        self.temperature_target = settings_dict["temperature_target"]
        self.refresh_interval_ms = settings_dict["refresh_interval_ms"]
        self.weather_service = settings_dict["weather_service"]
        self.lat = settings_dict["lat"]
        self.lon = settings_dict["lon"]

class SettingsFactory():
    @staticmethod
    def create_settings(path):
        settings = Settings(path)
        settings.load()
        return settings
