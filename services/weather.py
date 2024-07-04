import requests
from typing import Any
import pprint
import datetime


class WeatherOpenMeteo:
    URL: str = "https://api.open-meteo.com/v1/forecast"

    _weather_code = {
        0: 'Ясно',
        1: 'В основном ясно',
        2: 'Переменная облачность',
        3: 'Пасмурно',
        45: 'Туман',
        48: 'Изморозь',
        51: 'Слабая морось',
        53: 'Морось',
        55: 'Интенсивная морось',
        56: 'Морось со снегом',
        57: 'Интенсивная морось со снегом',
        61: 'Слабый дождь',
        63: 'Дождь',
        65: 'Сильный дождь',
        66: 'Ледяной дождь',
        67: 'Интенсивный ледяной дождь',
        71: 'Небольшой снегопад',
        73: 'Снегопад',
        75: 'Сильный снегопад',
        77: 'Снег крупинками',
        80: 'Небольшой ливень',
        81: 'Ливень',
        82: 'Сильный ливень',
        85: 'Дождь со снегом',
        86: 'Сильный дождь со снегом',
        95: 'Гроза',
        96: 'Гроза с небольшим градом',
        99: 'Гроза с сильным градом',
    }

    _params: dict[str, Any] = {
        'longitude':            0,
        'latitude':             0,
        'timezone':             'auto',
        'wind_speed_unit':      'ms',
        'temperature_unit':     'celsius',
        'precipitation_unit':   'mm',
        'forecast_days': 1,
    }
    params_15m: dict[str, Any] = _params.copy()
    params_h: dict[str, Any] = _params.copy()
    params_d: dict[str, Any] = _params.copy()

    def __init__(self):
        self.params_15m.update({
            'minutely_15': (
                'temperature_2m',               # температура
                'relative_humidity_2m',         # относительная влажность
                'apparent_temperature',         # температура по ощущениям
                'pressure_msl',                 # давление
                'wind_speed_10m',               # скорость ветра
                'wind_direction_10m',           # направление ветра
                'is_day',                       # True - день, False - ночь
                'weather_code',                 # код погоды
                'precipitation_probability',    # вероятность осадков %
                'precipitation',                # кол-во осадков мм
            ),
        })

        self.params_h.update({
            'hourly': (
                'temperature_2m',               # температура
                'relative_humidity_2m',         # относительная влажность
                'apparent_temperature',         # температура по ощущениям
                'pressure_msl',                 # давление
                'wind_speed_10m',               # скорость ветра
                'wind_direction_10m',           # направление ветра
                'is_day',                       # True - день, False - ночь
                'weather_code',                 # код погоды
                'precipitation_probability',    # вероятность осадков %
                'precipitation',                # кол-во осадков мм
            ),
        })

    @staticmethod
    def _is_coordinates(latitude: int | float, longitude: int | float) -> bool:
        if ((isinstance(latitude, int) or isinstance(latitude, float)) and
                (isinstance(longitude, int) or isinstance(longitude, float))):
            return True
        return False

    @staticmethod
    def _get_wind_direction(azimuth: int | float) -> str:
        while True:
            if 23 <= azimuth < 68:
                yield 'северо-восточный'
            if 68 <= azimuth < 113:
                yield 'восточный'
            if 113 <= azimuth < 158:
                yield 'юго-восточный'
            if 158 <= azimuth < 203:
                yield 'южный'
            if 203 <= azimuth < 225:
                yield 'юго-западный'
            if 225 <= azimuth < 248:
                yield 'западный'
            if 248 <= azimuth < 293:
                yield 'северо-западный'
            if 293 <= azimuth or azimuth < 23:
                yield 'северный'

    def get_current_weather(self, latitude: int | float, longitude: int | float) -> dict[str, Any]:
        if not (self._is_coordinates(latitude, longitude)):
            return 'Not coordinates'

        parameters = self.params_15m.copy()
        parameters['longitude'] = longitude
        parameters['latitude'] = latitude
        parameters['forecast_minutely_15'] = 1
        response = requests.get(self.URL, params=parameters).json()

        temperature = response['minutely_15']['temperature_2m'][0]
        apparent_temperature = response['minutely_15']['apparent_temperature'][0]
        relative_humidity = response['minutely_15']['relative_humidity_2m'][0]
        what_outside = self._weather_code[
            response['minutely_15']['weather_code'][0]]
        pressure = response['minutely_15']['pressure_msl'][0] * 0.75
        wind_speed = response['minutely_15']['wind_speed_10m'][0]
        wind_direction = next(self._get_wind_direction(
            response['minutely_15']['wind_direction_10m'][0]))
        # is_day = response['minutely_15']['is_day'][0]
        precipitation_probability = response['minutely_15']['precipitation_probability'][0]
        precipitation = response['minutely_15']['precipitation'][0]

        text: str = f'''
Погода сейчас: {what_outside}
Температура: {temperature}
По ощущениям: {apparent_temperature}

Влажность: {relative_humidity}%
Ветер {wind_direction}, {wind_speed} м/с
Давление: {pressure:.5} мм рт.ст.'''
        if precipitation_probability > 0:
            text += f'''\nВероятность осадков: {precipitation_probability}%'''
        return text

    def get_daily_forecast(self, latitude: int | float, longitude: int | float) -> dict[str, Any]:
        if not (self._is_coordinates(latitude, longitude)):
            return 'Not coordinates'

        parameters = self.params_h.copy()
        parameters['longitude'] = longitude
        parameters['latitude'] = latitude
        parameters['forecast_days'] = 1
        response = requests.get(self.URL, params=parameters).json()

        r = response['hourly']
        text = f'Погода на сегодня:\n'
        p = sum(r['pressure_msl']) / len(r['pressure_msl']) * 0.75
        text += f'Давление: {p:0.1f}\n'
        h = sum(r['relative_humidity_2m']) / len(r['relative_humidity_2m'])
        text += f'Влажность: {h:0.1f}%\n'
        for i in range(7, len(r['time'])):
            string = ''
            string += f'''{r['time'][i][-5:]}: {r['temperature_2m'][i]}°C, {
                r['wind_speed_10m'][i]} м/с, {self._weather_code[r['weather_code'][i]]}'''
            text += string + '\n'
        return text

    def get_weekly_forecast(self, latitude: int | float, longitude: int | float) -> dict[str, Any]:
        if not (self._is_coordinates(latitude, longitude)):
            return 'Not coordinates'

        parameters = self.params_h.copy()
        parameters['longitude'] = longitude
        parameters['latitude'] = latitude
        parameters['forecast_days'] = 7
        parameters['daily'] = ('weather_code', )
        response = requests.get(self.URL, params=parameters).json()

        r = response['hourly']
        text = f'''Прогноз на неделю:\n'''
        day = 0
        weekday_dict = {
            0:  'Пн', 1:  'Вт',  2:  'Ср',  3:  'Чт',  4:  'Пт',  5:  'Сб',  6:  'Вс'}
        while day != parameters['forecast_days']:
            string = ''

            date = datetime.datetime.fromisoformat(
                r['time'][day * 24])
            weekday = date.weekday()
            date = f"{weekday_dict[weekday]} {
                date.day}.{date.month}.{date.year}"
            string += f"{date:>9}: "

            t = (min(r['temperature_2m'][day*24:(day+1)*24]
                     ), max(r['temperature_2m'][day*24:(day+1)*24]))
            string += f'{str(t[0]):>5}..{str(t[1]):>5}°C, '

            p = sum(r['pressure_msl'][day*24:(day+1)*24]) / 24 * 0.75
            string += f'{(p):0.1f}, '

            string += f'{self._weather_code[response['daily']
                                            ['weather_code'][day]]}\n'

            text += string
            day += 1
        return text


if __name__ == '__main__':
    w = WeatherOpenMeteo()
    # print(w.get_daily_forecast(54.7431, 55.9678))
    print(w.get_weekly_forecast(54.7431, 55.9678))
