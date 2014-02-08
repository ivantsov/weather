from django.db import models


class Weather(models.Model):
	WEATHER_SERVICE = (
		('YX', 'yandex'),
		('YO', 'yahoo'),
	)

	service = models.CharField(max_length=2, choices=WEATHER_SERVICE)
	city_id = models.CharField(max_length=10)
	city_name = models.CharField(max_length=100)
	temperature = models.IntegerField()
	pressure = models.IntegerField()
	humidity = models.IntegerField()
	last_update = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return '%d - %s - %s' % (self.pk, self.service, self.city_name)
