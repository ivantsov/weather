# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from app.models import YandexWeather, YahooWeather, YANDEX_CITY_LIST, YAHOO_CITY_LIST
from app.weather_parsers import YandexWeatherParser, YahooWeatherParser

class Command(BaseCommand):
	args = ''
	help = 'Get new weather data and add that into database'

	def handle(self, *args, **options):
		yandex_wp = YandexWeatherParser('http://export.yandex.ru/weather-ng/forecasts/%s.xml', YANDEX_CITY_LIST)
		yandex_weather = yandex_wp.getWeather()

		yahoo_wp = YahooWeatherParser('http://weather.yahooapis.com/forecastrss?p=%s&u=c', YAHOO_CITY_LIST)
		yahoo_weather = yahoo_wp.getWeather()

		for city in (yandex_weather + yahoo_weather):
			data = {
				'city_id': city['id'],
				'city_name': city['name'],
				'temperature': city['temperature'],
				'pressure': city['pressure'],
				'humidity': city['humidity']
			}

			if city['id'] in YANDEX_CITY_LIST:
				w = YandexWeather(**data)
			elif city['id'] in YAHOO_CITY_LIST:
				w = YahooWeather(**data)

			w.save()