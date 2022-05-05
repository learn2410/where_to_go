import json

from django.conf import settings
from django.shortcuts import render, HttpResponse, get_object_or_404

from .models import Place


def geojson_feature(place):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [place.lng, place.lat]
        },
        "properties": {
            "title": place.title,
            "placeId": str(place.id),
            "detailsUrl": place.get_place_json_url()
        }
    }


def get_place_json(place):
    image_urls = [f'{settings.MEDIA_URL}{s}'
                  for s in place.images.order_by('number').values_list('img', flat=True)]

    payload_place = {"title": place.title,
                     "imgs": image_urls,
                     "description_short": place.description_short,
                     "description_long": place.description_long,
                     "coordinates": {
                         "lng": place.lng,
                         "lat": place.lat
                     }
                     }
    return json.dumps(payload_place, ensure_ascii=False)


def make_geodict(dataset):
    return {"type": "FeatureCollection", "features": [geojson_feature(row) for row in dataset]}


def view_blank(request):
    places = Place.objects.all()
    content = {'geodict': make_geodict(places)}
    return render(request, 'places/pindex.html', content)


def detail_json(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    content = get_place_json(place)
    return HttpResponse(content, content_type='application/json')
