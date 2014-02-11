from django.db import models


class Weather(models.Model):
	city_name = models.CharField(max_length=100)
	temperature = models.IntegerField()
	pressure = models.IntegerField()
	humidity = models.IntegerField()
	last_update = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

	def __unicode__(self):
		return '%d - %s' % (self.pk, self.city_name)


class YandexWeather(Weather):
	city_id = models.PositiveIntegerField()


class YahooWeather(Weather):
	city_id = models.CharField(max_length=10)