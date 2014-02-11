# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
import requests
from xml.dom import minidom
from xml.parsers.expat import ExpatError

from app.models import YandexWeather, YahooWeather, YANDEX_CITY_LIST, YAHOO_CITY_LIST

__metaclass__ = type

class WeatherParser:
	def __init__(self, url, city_list):
		self.city_list = city_list
		self.url = url
		self.xml = {}
		self.weather = []

	def loadXml(self):
		for city in self.city_list:
			self.xml[city] = requests.get(self.url % city).content

	def getWeather(self):
		self.loadXml()

		try:
			self.parse()
		except ExpatError as e:
			print 'Parse error: %s' % e
		except IndexError as e:
			print 'Data for parsing is empty: %s' % e

		return self.weather


class YandexWeatherParser(WeatherParser):
	def __init__(self, url, city_list):
		super(YandexWeatherParser, self).__init__(url, city_list)

	def parse(self):
		for city in self.city_list:
			dom = minidom.parseString(self.xml[city])

			parse_data = {
				u'id': city,
				u'name': dom.getElementsByTagName(u'forecast')[0].getAttribute(u'city'),
				u'temperature': dom.getElementsByTagName(u'temperature')[0].firstChild.nodeValue,
				u'pressure': dom.getElementsByTagName(u'pressure')[0].firstChild.nodeValue,
				u'humidity': dom.getElementsByTagName(u'humidity')[0].firstChild.nodeValue
			}

			self.weather.append(parse_data)


class YahooWeatherParser(WeatherParser):
	def __init__(self, url, city_list):
		super(YahooWeatherParser, self).__init__(url, city_list)

	def parse(self):
		for city in self.city_list:
			dom = minidom.parseString(self.xml[city])

			parse_data = {
				u'id': city,
				u'name': dom.getElementsByTagName(u'yweather:location')[0].getAttribute(u'city'),
				u'temperature': dom.getElementsByTagName(u'yweather:condition')[0].getAttribute(u'temp'),
				u'pressure': int(float(dom.getElementsByTagName(u'yweather:atmosphere')[0].getAttribute(u'pressure')) * 0.75),
				u'humidity': dom.getElementsByTagName(u'yweather:atmosphere')[0].getAttribute(u'humidity')
			}

			self.weather.append(parse_data)


class Command(BaseCommand):
	args = ''
	help = 'Get new weather data and add that into database'

	def handle(self, *args, **options):
		yandex_wp = YandexWeatherParser(u'http://export.yandex.ru/weather-ng/forecasts/%s.xml', YANDEX_CITY_LIST)
		yandex_weather = yandex_wp.getWeather()

		for city in yandex_weather:
			w = YandexWeather(
				city_id = city['id'],
				city_name = city['name'],
				temperature = city['temperature'],
				pressure = city['pressure'],
				humidity = city['humidity']
			)

			w.save()

		yahoo_wp = YahooWeatherParser(u'http://weather.yahooapis.com/forecastrss?p=%s&u=c', YAHOO_CITY_LIST)
		yahoo_weather = yahoo_wp.getWeather()

		for city in yahoo_weather:
			w = YahooWeather(
				city_id = city['id'],
				city_name = city['name'],
				temperature = city['temperature'],
				pressure = city['pressure'],
				humidity = city['humidity']
			)

			w.save()
