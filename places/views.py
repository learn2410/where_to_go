from django.shortcuts import render, HttpResponse, get_object_or_404

from .models import Place


def make_geodict(dataset):
    return {"type": "FeatureCollection", "features": [row.geojson_feature for row in dataset]}


def view_blank(request):
    places = Place.objects.all()
    content = {'geodict': make_geodict(places)}
    return render(request, 'places/pindex.html', content)


def detail_json(request, idfromurl):
    p = get_object_or_404(Place, pk=idfromurl)
    d = p.get_place_json()
    return HttpResponse(d, content_type='application/json')
