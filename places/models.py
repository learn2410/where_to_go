from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name="заголовок")
    description_short = models.CharField(max_length=256, null=False, blank=True, verbose_name="короткое описание")
    description_long = models.TextField(null=False, blank=True, verbose_name="длинное описание")
    lng = models.FloatField(verbose_name="долгота")
    lat = models.FloatField(verbose_name="широта")
