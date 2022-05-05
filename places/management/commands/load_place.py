import logging
import os
from urllib.parse import urlparse

import requests
from PIL import Image as Pil_Image
from django.conf import settings
from django.core.management.base import BaseCommand
from pathvalidate import sanitize_filename

from places.models import Place, Image


def optimize_image(image_path):
    size = 1200, 800
    with Pil_Image.open(image_path) as im:
        im.thumbnail(size)
        im.save(image_path)


def get_image(img_url, save_path):
    os.makedirs(save_path, exist_ok=True)
    img_filename = sanitize_filename(urlparse(img_url).path.split('/')[-1])
    img_filepath = os.path.normcase(os.path.join(save_path, img_filename))
    response = requests.get(img_url, allow_redirects=False)
    response.raise_for_status()
    with open(img_filepath, 'wb') as file:
        file.write(response.content)
    optimize_image(img_filepath)
    return img_filename


def load_place(json_url):
    response = requests.get(json_url)
    response.raise_for_status()
    new_place = response.json()
    if not ({'title', 'description_long', 'coordinates', 'description_short'}.issubset(set(new_place.keys()))
            and {'lng', 'lat'}.issubset(set(new_place['coordinates'].keys()))):
        logging.warning(f"response does not contain required field, place didn't load\n\t url={json_url}")
        return
    tmp_dir = os.path.join(settings.MEDIA_ROOT, 'tmp')
    img_dir = os.path.join(settings.MEDIA_ROOT, 'image')
    os.makedirs(img_dir, exist_ok=True)
    Place.objects.filter(title=new_place['title']).delete()
    place, _status = Place.objects.get_or_create(
        title=new_place['title'],
        defaults={
            'description_short': new_place['description_short'],
            'description_long': new_place['description_long'],
            'lng': new_place['coordinates']['lng'],
            'lat': new_place['coordinates']['lat']
        }
    )
    new_images = []
    for img_url in new_place['imgs']:
        img_filename = get_image(img_url, tmp_dir)
        os.replace(os.path.join(tmp_dir, img_filename), os.path.join(img_dir, img_filename))
        new_images.append(Image(place_id=place.pk, img=f'image/{img_filename}'))
    Image.objects.bulk_create(new_images)


class Command(BaseCommand):
    help = u'Импорт места по ссылке на json'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str, help=self.help)

    def handle(self, *args, **kwargs):
        url = kwargs['json_url']
        load_place(url)
