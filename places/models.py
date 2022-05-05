from django.db import models
from django.urls import reverse
from tinymce import models as tinymce_models


class Place(models.Model):
    title = models.CharField(verbose_name="заголовок", max_length=100, unique=True)
    description_short = models.TextField(verbose_name="краткое описание", blank=True)
    description_long = tinymce_models.HTMLField(verbose_name="подробное описание", blank=True)
    lng = models.FloatField(verbose_name="долгота")
    lat = models.FloatField(verbose_name="широта")

    def __str__(self):
        return self.title

    def get_place_json_url(self):
        return reverse('places:json_place', args=[self.pk])

    class Meta(object):
        verbose_name = 'МЕСТО'
        verbose_name_plural = 'МЕСТА'


class Image(models.Model):
    number = models.PositiveIntegerField("номер", default=0)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(verbose_name="фотография", upload_to='image')

    @property
    def place_num(self):
        return '{} - {}'.format(self.number, self.place)

    def __str__(self):
        return self.place_num

    class Meta(object):
        ordering = ['number']
        verbose_name = 'ФОТО'
        verbose_name_plural = 'ФОТОГРАФИИ'
