import requests


class WeatherServiceException(Exception):
    pass


class WeatherService:
    GEO_URL = 'https://geocoding-api.open-meteo.com/v1/search'
    WEATHER_URL = 'https://api.open-meteo.com/v1/forecast'

    @staticmethod
    def get_geo_data(city_name):
        params = {
            'name': city_name
        }
        res = requests.get(f'{WeatherService.GEO_URL}', params=params)
        if res.status_code != 200:
            raise WeatherServiceException('Can not get geo data.')
        elif not res.json().get('results'):
            raise WeatherServiceException('City not found.')

        # print(res.json())
        return res.json().get('results')

    @staticmethod
    def get_current_weather_by_geo_data(lat, lon):
        params = {
            'latitude': lat,
            'longitude': lon,
            'current_weather': True
        }
        res = requests.get(f'{WeatherService.WEATHER_URL}', params=params)
        if res.status_code != 200:
            raise WeatherServiceException('Can not get geo data.')
        # print(res.json().get('current_weather'))
        current_res = res.json().get('current_weather')

        answer = f"Current weather: \n" \
                 f"temperature - {current_res.get('temperature')} degree(s) Celsius, \n" \
                 f"windspeed - {current_res.get('windspeed')} hm/h, \n" \
                 f"winddirection - {current_res.get('winddirection')} degree(s)."

        return answer
