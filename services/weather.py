import requests
import pprint
from typing import Any

URL = "https://api.open-meteo.com/v1/forecast"
params = {
    'hourly': ('temperature_2m', 'wind_speed_10m', 'surface_pressure'),
    'forecast_days': 1,
    'wind_speed_unit': 'ms',
    'minutely_15': 'temperature_2m',
    'forecast_minutely_15': 1,
    'past_minutely_15': 0,
    'timezone': 'auto',
}


def _is_coordinates(latitude: int | float, longitude: int | float) -> bool:
    if ((isinstance(latitude, int) or isinstance(latitude, float)) and
            (isinstance(longitude, int) or isinstance(longitude, float))):
        return True
    return False


def get_weather_now(latitude=None, longitude=None) -> str:
    if not (_is_coordinates(latitude, longitude)):
        return 'Not coordinates'
    params = {
        'hourly': ('temperature_2m', 'wind_speed_10m', 'surface_pressure'),
        'forecast_days': 1,
        'wind_speed_unit': 'ms',
        'forecast_minutely_15': 24,
        'minutely_15': 'temperature_2m',
        'forecast_minutely_15': 1,
        'past_minutely_15': 0,
        'timezone': 'auto',
    }
    params['latitude'] = latitude
    params['longitude'] = longitude
    response = requests.get(URL, params=params).json()
    return str(response['minutely_15']['temperature_2m'][0])


if __name__ == '__main__':
    pprint.pprint(get_weather_now(54.7431, 55.9678))
