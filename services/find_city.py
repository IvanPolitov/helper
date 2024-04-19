import requests
from typing import Any, Tuple
import json


class City:
    URL = "https://geocoding-api.open-meteo.com/v1/search"
    _params = {}

    def __init__(self) -> None:
        _params = {
            'name': '',
            'count': 10,
            'format': 'json',
            'language': 'ru',
        }

    def find(self, name: str) -> Tuple[int | float, int | float]:
        self._params['name'] = name
        response = requests.get(self.URL, params=self._params).json()
        with open('data_file.json', 'w') as f:
            f.write(json.dumps(response, indent=4))
        return response


if __name__ == '__main__':
    city = City()
    print(city.find('Ufa'))
