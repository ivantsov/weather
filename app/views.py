# -*- coding: utf-8 -*-

from django.shortcuts import render

import requests
from xml.dom import minidom

from models import YandexWeather, YahooWeather

#chelyabinsk, moscow, petesburg
YANDEX_CITY_LIST = [28642, 27612, 26063]
YAHOO_CITY_LIST = ['RSXX0024', 'RSXX0063', 'RSXX0091']

__metaclass__ = type

class WeatherParser:
	def __init__(self, url, city_list):
		self.city_list = city_list
		self.url = url
		self.dom = {}
		self.weather = []

	def loadXml(self):
		for city in self.city_list:
			self.dom[city] = minidom.parseString(requests.get(self.url % city).content)

	def getWeather(self):
		self.loadXml()
		self.parse()

		return self.weather


class YandexWeatherParser(WeatherParser):
	def __init__(self, url, city_list):
		super(YandexWeatherParser, self).__init__(url, city_list)

	def parse(self):
		for city in self.city_list:
			parse_data = {
				u'id': city,
				u'name': self.dom[city].getElementsByTagName(u'forecast')[0].getAttribute(u'city'),
				u'temperature': self.dom[city].getElementsByTagName(u'temperature')[0].firstChild.nodeValue,
				u'pressure': self.dom[city].getElementsByTagName(u'pressure')[0].firstChild.nodeValue,
				u'humidity': self.dom[city].getElementsByTagName(u'humidity')[0].firstChild.nodeValue
			}

			self.weather.append(parse_data)


class YahooWeatherParser(WeatherParser):
	def __init__(self, url, city_list):
		super(YahooWeatherParser, self).__init__(url, city_list)

	def parse(self):
		for city in self.city_list:
			parse_data = {
				u'id': city,
				u'name': self.dom[city].getElementsByTagName(u'yweather:location')[0].getAttribute(u'city'),
				u'temperature': self.dom[city].getElementsByTagName(u'yweather:condition')[0].getAttribute(u'temp'),
				u'pressure': int(float(self.dom[city].getElementsByTagName(u'yweather:atmosphere')[0].getAttribute(u'pressure')) * 0.75),	#convert from US to EU measure of pressure
				u'humidity': self.dom[city].getElementsByTagName(u'yweather:atmosphere')[0].getAttribute(u'humidity')
			}

			self.weather.append(parse_data)

# def getWeather(request):
# 	yandexWeatherParser = YandexWeatherParser(u'http://export.yandex.ru/weather-ng/forecasts/%s.xml', YANDEX_CITY_LIST)
#
# 	print yandexWeatherParser.getWeather()

# def updateWeather(request):
# 	if request.method == 'POST':
# 		yandex_weather = getWeather(1, yandex_city_list)
# 		yahoo_weather = getWeather(2, yahoo_city_list)
#
# 		for city in yandex_weather:
# 			w = Weather(
# 				service = u'YX',
# 				city_id = city['id'],
# 				city_name = city['name'],
# 				temperature = city['temperature'],
# 				pressure = city['pressure'],
# 				humidity = city['humidity']
# 			)
#
# 			w.save()
#
# 		for city in yahoo_weather:
# 			w = Weather(
# 				service = u'YO',
# 				city_id = city['id'],
# 				city_name = city['name'],
# 				temperature = city['temperature'],
# 				pressure = city['pressure'],
# 				humidity = city['humidity']
# 			)
#
# 			w.save()
#
# 		return HttpResponseRedirect('/')


def index(request):
	yandex_weather = []
	yahoo_weather = []

	try:
		for city in YANDEX_CITY_LIST:
			yandex_weather.append(YandexWeather.objects.filter(city_id=city).order_by('-pk')[0])

		for city in YAHOO_CITY_LIST:
			yahoo_weather.append(YahooWeather.objects.filter(city_id=city).order_by('-pk')[0])
	except IndexError:
		print 'Empty Database'

	return render(request, u'base.html', {u'yandex_weather': yandex_weather, u'yahoo_weather': yahoo_weather})