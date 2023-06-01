import requests


class WeatherServiceException(Exception):
    pass


class WeatherService:
    """
    This is a class that provides weather data for a given city. It has two static variables, GEO_URL and WEATHER_URL, 
    which are the URLs for the geocoding and weather APIs respectively. It has one static method, get_geo_data,
    which takes a city name as input and returns the current weather data for that city.
    It first sends a request to the geocoding API to get the latitude and longitude of the city,
    and then sends a request to the weather API to get the current weather data for that location.
    If the request to the geocoding API fails, it raises a WeatherServiceException.
    If the request to the weather API succeeds, it returns a string containing the current temperature, wind speed,
    and wind direction for
    """
    GEO_URL = 'https://geocoding-api.open-meteo.com/v1/search'
    WEATHER_URL = 'https://api.open-meteo.com/v1/forecast'

    @staticmethod
    def get_geo_data(city_name):
        """
        This is a static method that retrieves the geographic data for a given city name.
        :param city_name - the name of the city to retrieve data for
        :return the geographic data for the city
        """
        params = {
            'name': city_name
        }
        res = requests.get(f'{WeatherService.GEO_URL}', params=params)
        if res.status_code != 200:
            raise WeatherServiceException('Can not get geo data.')
        elif not res.json().get('results'):
            raise WeatherServiceException('City not found.')

        return res.json().get('results')

    @staticmethod
    def get_current_weather_by_geo_data(lat, lon):
        """
        This is a static method that retrieves the current weather data for a given latitude and longitude.
        :param lat - the latitude of the location
        :param lon - the longitude of the location
        :return a string containing the current weather data for the given location.
        The string contains the temperature, wind speed, and wind direction.
        """
        params = {
            'latitude': lat,
            'longitude': lon,
            'current_weather': True
        }
        res = requests.get(f'{WeatherService.WEATHER_URL}', params=params)
        if res.status_code != 200:
            raise WeatherServiceException('Can not get geo data.')
        current_res = res.json().get('current_weather')

        answer = f"Current weather: \n" \
                 f"temperature - {current_res.get('temperature')} °C, \n" \
                 f"wind speed - {current_res.get('windspeed')} km/h, \n" \
                 f"wind direction - {current_res.get('winddirection')} degree(s)."

        return answer
