# -*- coding: utf-8 -*-

from django.shortcuts import render

from models import YandexWeather, YahooWeather, YANDEX_CITY_LIST, YAHOO_CITY_LIST

def index(request):
	yandex_weather = {'name': u'Яндекс', 'city_list': []}
	yahoo_weather = {'name': u'Yahoo', 'city_list': []}

	try:
		for city in YANDEX_CITY_LIST:
			yandex_weather['city_list'].append(YandexWeather.objects.filter(city_id=city).order_by('-pk')[0])

		for city in YAHOO_CITY_LIST:
			yahoo_weather['city_list'].append(YahooWeather.objects.filter(city_id=city).order_by('-pk')[0])
	except IndexError:
		print 'Empty database'

	weather = (yandex_weather, yahoo_weather)

	return render(request, u'base.html', {u'weather': weather})