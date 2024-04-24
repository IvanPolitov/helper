import requests
from typing import Any, Tuple
import json
from urllib.parse import quote


class City:
    URL = "https://geocoding-api.open-meteo.com/v1/search"
    _params = {}

    def __init__(self) -> None:
        self._params = {
            'name': '',
            'count': 10,
            'format': 'json',
            'language': 'ru',
        }

    def find(self, name: str) -> Tuple[int | float, int | float]:
        self._params['name'] = name
        response = requests.get(self.URL, params=self._params)

        with open("data_file.json", 'w') as f:
            json.dump(response.json(), f, indent=4)

        if response.status_code == 200:
            response = response.json()

            if response.get('results'):
                latitude = response['results'][0]["latitude"]
                longitude = response['results'][0]["longitude"]
                return latitude, longitude
        return None, None


if __name__ == '__main__':
    city = City()
    print(city.find('Уфа'))
