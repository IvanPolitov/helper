from typing import Tuple
from dadata import Dadata
import pprint


class Geocoding():
    token = 'd67b3517346f9f93dac0a6a1743672dd44d032b8'
    secret = 'e352c2603927fcc379c574f22595de709bacd433'

    def find_name(self, latitude: int | float, longitude: int | float) -> str:
        da = Dadata(token=self.token, secret=self.secret)
        res = da.geolocate(name="address", lat=latitude,
                           lon=longitude, count=1)
        da.close()
        print(res)
        if res:
            res = f'{res[0]['data']['city']}, {res[0]['data']['country']}'
        return res

    def find_coord(self, name: str) -> Tuple[int | float, int | float]:
        da = Dadata(token=self.token, secret=self.secret)
        res = da.clean(name='address', source=name,)
        da.close()
        return res['result'], float(res['geo_lat']), float(res['geo_lon'])


if __name__ == '__main__':
    geocode = Geocoding()
    print(geocode.find_name(54.734856, 55.9577802))
    # print(geocode.find_coord('УФА'))
    # print(geocode.find_coord('Москва'))
