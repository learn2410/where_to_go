import json
import os
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from pathvalidate import sanitize_filename

from places.models import Place, Image
from PIL import Image as pil_image

def get_place(url):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    return None if response.is_redirect else json.loads(response.text.replace('\n', ''))


def optimize_image(image_path):
    max_size = (1200, 800)
    img = pil_image.open(image_path)
    width,height=img.size
    k=max(1,min(width/max_size[0],height/max_size[1]))
    img=img.resize((int(width/k),int(height/k)))
    img.save(image_path)


def get_image(img_url):
    tmp_dir = os.path.join(settings.MEDIA_ROOT, 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)
    img_filename = sanitize_filename(urlparse(img_url).path.split('/')[-1])
    img_filepath = os.path.normcase(os.path.join(tmp_dir, img_filename))
    response = requests.get(img_url, allow_redirects=False)
    response.raise_for_status()
    with open(img_filepath, 'wb') as file:
        file.write(response.content)
    optimize_image(img_filepath)
    return img_filename


def verify_json(place):
    required_fields = {'title', 'description_long', 'coordinates', 'description_short'}
    return (required_fields.issubset(set(place.keys()))
            and {'lng', 'lat'}.issubset(set(place['coordinates'].keys())))


def append_place(json_url):
    response = requests.get(json_url, allow_redirects=False)
    response.raise_for_status()
    if response.is_redirect:
        return
    newplace = json.loads(response.text.replace('\n', ''))
    if not verify_json(newplace):
        return
    tmp_dir = os.path.join(settings.MEDIA_ROOT, 'tmp')
    img_dir = os.path.join(settings.MEDIA_ROOT, 'image')
    Place.objects.filter(title=newplace['title']).delete()
    obj, _created = Place.objects.get_or_create(
        title=newplace['title'],
        defaults={
            'description_short': newplace['description_short'],
            'description_long': newplace['description_long'],
            'lng': newplace['coordinates']['lng'],
            'lat': newplace['coordinates']['lat']
        }
    )
    obj.save()
    for i in newplace['imgs']:
        im = get_image(i)
        os.replace(os.path.join(tmp_dir, im), os.path.join(img_dir, im))
        ii = Image.objects.create(placeid_id=obj.pk, img=f'image/{im}')
        ii.save()


class Command(BaseCommand):
    help = u'Импорт места по ссылке на json'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str, help=self.help)

    def handle(self, *args, **kwargs):
        url = kwargs['json_url']
        append_place(url)
