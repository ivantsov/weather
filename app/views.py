# -*- coding: utf-8 -*-

from django.shortcuts import render

import requests
from xml.dom import minidom

from models import YandexWeather, YahooWeather

#chelyabinsk, moscow, petesburg
yandex_city_list = [28642, 27612, 26063]
yahoo_city_list = ['RSXX0024', 'RSXX0063', 'RSXX0091']


#service1 - yandex, service2 - yahoo
# def getWeather(service, city_list):
# 	weather = []
#
# 	for city in city_list:
# 		if service == 1:
# 			url = u'http://export.yandex.ru/weather-ng/forecasts/%s.xml' % city
# 		else:
# 			url = u'http://weather.yahooapis.com/forecastrss?p=%s&u=c' % city
#
# 		dom = minidom.parseString(requests.get(url).content)
#
# 		if service == 1:
# 			city_weather = {
# 				u'id': city,
# 				u'name': dom.getElementsByTagName(u'forecast')[0].getAttribute(u'city'),
# 				u'temperature': dom.getElementsByTagName(u'temperature')[0].firstChild.nodeValue,
# 				u'pressure': dom.getElementsByTagName(u'pressure')[0].firstChild.nodeValue,
# 				u'humidity': dom.getElementsByTagName(u'humidity')[0].firstChild.nodeValue
# 			}
# 		else:
# 			city_weather = {
# 				u'id': city,
# 				u'name': dom.getElementsByTagName(u'yweather:location')[0].getAttribute(u'city'),
# 				u'temperature': dom.getElementsByTagName(u'yweather:condition')[0].getAttribute(u'temp'),
# 				u'pressure': int(float(dom.getElementsByTagName(u'yweather:atmosphere')[0].getAttribute(u'pressure')) * 0.75),	#convert from US to EU measure of pressure
# 				u'humidity': dom.getElementsByTagName(u'yweather:atmosphere')[0].getAttribute(u'humidity')
# 			}
#
# 		weather.append(city_weather)
#
# 	return weather

# def getYandexWeather():
# 	weather = []
#
# 	for city in yandex_city_list:
# 		r = requests.get(u'http://export.yandex.ru/weather-ng/forecasts/%s.xml' % city)
# 		dom = minidom.parseString(r.content)
#
# 		city_weather = {
# 			u'id': city,
# 			u'name': dom.getElementsByTagName(u'forecast')[0].getAttribute(u'city'),
# 			u'temperature': dom.getElementsByTagName(u'temperature')[0].firstChild.nodeValue,
# 			u'pressure': dom.getElementsByTagName(u'pressure')[0].firstChild.nodeValue,
# 			u'humidity': dom.getElementsByTagName(u'humidity')[0].firstChild.nodeValue
# 		}
#
# 		weather.append(city_weather)
#
# 	return weather
#
#
# def getYahooWeather():
# 	weather = []
#
# 	for city in yahoo_city_list:
# 		r = requests.get(u'http://weather.yahooapis.com/forecastrss?p=%s&u=c' % city)
# 		dom = minidom.parseString(r.content)
#
# 		city_weather = {
# 			u'id': city,
# 			u'name': dom.getElementsByTagName(u'yweather:location')[0].getAttribute(u'city'),
# 			u'temperature': dom.getElementsByTagName(u'yweather:condition')[0].getAttribute(u'temp'),
# 			u'pressure': int(float(dom.getElementsByTagName(u'yweather:atmosphere')[0].getAttribute(u'pressure')) * 0.75),
# 			u'humidity': dom.getElementsByTagName(u'yweather:atmosphere')[0].getAttribute(u'humidity')
# 		}
#
# 		weather.append(city_weather)
#
# 	return weather

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
		for city in yandex_city_list:
			yandex_weather.append(YandexWeather.objects.filter(city_id=city).order_by('-pk')[0])

		for city in yahoo_city_list:
			yahoo_weather.append(YahooWeather.objects.filter(city_id=city).order_by('-pk')[0])
	except IndexError:
		print 'Empty Database'

	return render(request, u'base.html', {u'yandex_weather': yandex_weather, u'yahoo_weather': yahoo_weather})