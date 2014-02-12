# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.management import call_command

from models import YandexWeather, YahooWeather, YANDEX_CITY_LIST, YAHOO_CITY_LIST
from weather_parsers import YandexWeatherParser, YahooWeatherParser

class WeatherParserTests(TestCase):
	def test_updateWeather(self):
		"""
		После вызова команды 'update_weather' количество записей в бд должно увеличиться на N для каждого сервиса, где N количество городов
		"""
		recordsYandexBefore = YandexWeather.objects.count()
		recordsYahooBefore = YahooWeather.objects.count()

		call_command('update_weather')

		recordsYandexAfter = YandexWeather.objects.count()
		recordsYahooAfter = YahooWeather.objects.count()

		self.assertEqual(recordsYandexBefore + len(YANDEX_CITY_LIST), recordsYandexAfter)
		self.assertEqual(recordsYahooBefore + len(YAHOO_CITY_LIST), recordsYahooAfter)