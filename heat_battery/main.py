import sys
from heat_battery import HeatBattery


def main():
    settings_path = sys.argv[1]
    heat_battery_obj = HeatBattery(settings_path)
    heat_battery_obj.start()


if __name__ == '__main__':
    main()
