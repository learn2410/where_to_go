import json

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from tinymce import models as tinymce_models


class Place(models.Model):
    title = models.CharField(max_length=100, null=False, blank=True)
    description_short = models.CharField(max_length=256, null=False, blank=True)
    description_long = tinymce_models.HTMLField(null=False, blank=True)
    lng = models.FloatField(verbose_name="долгота")
    lat = models.FloatField(verbose_name="широта")
    slug = models.AutoField

    def __str__(self):
        return self.title

    @property
    def geojson_feature(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.lng, self.lat]
            },
            "properties": {
                "title": self.title,
                "placeId": str(self.id),
                "detailsUrl": self.get_place_json_url()
            }
        }

    def get_place_json_url(self):
        return reverse('places:json_place', args=[self.pk])

    def get_place_json(self):
        im = list(map(lambda s: settings.MEDIA_URL + s,
                      Image.objects.filter(placeid=self.pk).order_by('number').values_list('img', flat=True)))
        # print(im)
        # TODO images urls
        d = {"title": self.title,
             "imgs": im,
             "description_short": self.description_short,
             "description_long": self.description_long,
             "coordinates": {
                 "lng": self.lng,
                 "lat": self.lat
             }
             }
        # print('*** d=',d)
        return json.dumps(d, ensure_ascii=False)

    class Meta(object):
        verbose_name = 'МЕСТО'
        verbose_name_plural = 'МЕСТА'



class Image(models.Model):
    number = models.PositiveIntegerField("номер", default=0, blank=False, null=False)
    placeid = models.ForeignKey(Place, on_delete=models.CASCADE, null=False)
    img = models.ImageField(upload_to='image')

    @property
    def place_num(self):
        return '{} - {}'.format(self.number, self.placeid)

    @property
    def img_preview(self):
        if self.img:
            return mark_safe('<img src="{}" height="200" />'.format(self.img.url))
        return ""

    def __str__(self):
        return self.place_num

    class Meta(object):
        ordering = ['number']
        verbose_name = 'ФОТО'
        verbose_name_plural = 'ФОТОГРАФИИ'
