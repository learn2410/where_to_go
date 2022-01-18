from django.db import models
from django.utils.html import mark_safe


class Place(models.Model):
    title = models.CharField(max_length=100, null=False, blank=True)
    description_short = models.CharField(max_length=256, null=False, blank=True)
    description_long = models.TextField(null=False, blank=True)
    lng = models.FloatField(verbose_name="долгота")
    lat = models.FloatField(verbose_name="широта")

    def __str__(self):
        return self.title


class Image(models.Model):
    placeid = models.ForeignKey(Place, on_delete=models.CASCADE, null=False)
    number = models.IntegerField("номер", default=0)
    img = models.ImageField(upload_to='image')

    @property
    def place_num(self):
        return '{} - {}'.format(self.number, self.placeid)

    @property
    def img_preview(self):
        if self.img:
            return mark_safe('<img src="{}" height="140" />'.format(self.img.url))
        return ""
