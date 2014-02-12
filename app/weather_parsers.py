import requests
from xml.dom import minidom
from xml.parsers.expat import ExpatError

__metaclass__ = type

class WeatherParser:
	def __init__(self, url, city_list):
		self.city_list = city_list
		self.url = url
		self.xml = {}
		self.weather = []

	def loadXml(self):
		for city in self.city_list:
			r = requests.get(self.url % city)

			if r.status_code != 200:
				raise RuntimeWarning('Can not load data from service')

			self.xml[city] = r.content

	def getWeather(self):
		try:
			self.loadXml()
		except RuntimeWarning as e:
			print e

		try:
			self.parse()
		except ExpatError as e:
			print 'Parse error: %s' % e
		except (IndexError, KeyError) as e:
			print 'Data for parsing is empty %s' % e

		return self.weather


class YandexWeatherParser(WeatherParser):
	def __init__(self, url, city_list):
		super(YandexWeatherParser, self).__init__(url, city_list)

	def parse(self):
		for city in self.city_list:
			dom = minidom.parseString(self.xml[city])

			parse_data = {
				'id': city,
				'name': dom.getElementsByTagName('forecast')[0].getAttribute('city'),
				'temperature': dom.getElementsByTagName('temperature')[0].firstChild.nodeValue,
				'pressure': dom.getElementsByTagName('pressure')[0].firstChild.nodeValue,
				'humidity': dom.getElementsByTagName('humidity')[0].firstChild.nodeValue
			}

			self.weather.append(parse_data)


class YahooWeatherParser(WeatherParser):
	def __init__(self, url, city_list):
		super(YahooWeatherParser, self).__init__(url, city_list)

	def parse(self):
		for city in self.city_list:
			dom = minidom.parseString(self.xml[city])

			parse_data = {
				'id': city,
				'name': dom.getElementsByTagName('yweather:location')[0].getAttribute('city'),
				'temperature': dom.getElementsByTagName('yweather:condition')[0].getAttribute('temp'),
				'pressure': int(float(dom.getElementsByTagName('yweather:atmosphere')[0].getAttribute('pressure')) * 0.75),
				'humidity': dom.getElementsByTagName('yweather:atmosphere')[0].getAttribute('humidity')
			}

			self.weather.append(parse_data)