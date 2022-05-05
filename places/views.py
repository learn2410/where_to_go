from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

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


def make_geodict(dataset):
    return {"type": "FeatureCollection", "features": [geojson_feature(row) for row in dataset]}


def view_blank(request):
    places = Place.objects.all()
    content = {'geodict': make_geodict(places)}
    return render(request, 'places/pindex.html', content)


def detail_json(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    image_urls = [f'{settings.MEDIA_URL}{s}'
                  for s in place.images.order_by('number').values_list('img', flat=True)]
    payload_place = {
        "title": place.title,
        "imgs": image_urls,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.lng,
            "lat": place.lat
        }
    }
    return JsonResponse(payload_place, json_dumps_params={'indent': 2, 'ensure_ascii': False})
