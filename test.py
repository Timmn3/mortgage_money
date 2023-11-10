from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder


def get_timezone(city_name):
    # Используем геокодер для получения координат города
    geolocator = Nominatim(user_agent="timezone_finder")
    location = geolocator.geocode(city_name)

    if location is not None:
        # Используем TimezoneFinder для определения часового пояса по координатам
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)

        return timezone_str
    else:
        return None


# Пример использования
city_name = input("Введите название города: ")
timezone = get_timezone(city_name)

if timezone:
    print(f"Часовой пояс для {city_name}: {timezone}")
else:
    print(f"Не удалось определить часовой пояс для {city_name}")
