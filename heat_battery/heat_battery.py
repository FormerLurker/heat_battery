import settings
import time
from weather import Weather

class HeatBattery():
    def __init__(self, settings_path):
        self.settings = settings.SettingsFactory.create_settings(settings_path)
        self.weather = Weather()

    def start(self):
        while True:
            time.sleep(self.settings.refresh_interval_ms/1000.0)
            temp = self.weather.get_current_temperature(
                self.settings.weather_service,
                self.settings.lat,
                self.settings.lon,
                self.settings.temperature_units
            )
            difference = abs(self.settings.temperature_target - temp)

            if difference < self.settings.temperature_variance:
                print("Time to dry!")
            else:
                print("Not time to dry!")


    def is_time_to_dry(self):
        return True

