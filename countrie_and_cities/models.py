from django.db import models
from django.urls import reverse


class Country(models.Model):

    country_title = models.CharField(max_length=250)
    country_info = models.TextField(max_length=1000)
    # is_selected = models.BooleanField(default=False, unique=False)

    def get_absolute_url(self):
        return reverse('country_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.country_title


class City(models.Model):

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city_title = models.CharField(max_length=250)
    city_info = models.TextField(max_length=1000)

    def get_absolute_url(self):
        return reverse('index')

    def __str__(self):
        return self.city_title
