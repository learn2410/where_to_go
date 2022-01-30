from django.shortcuts import render,HttpResponse, get_object_or_404
from .models import Place
import json

# Create your views here.
def make_geodict(dataset):
    return {"type": "FeatureCollection", "features": [row.geojson_feature for row in dataset]}


def view_blank(request):
    sss=' {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point","coordinates": [37.62, 55.793676]},"properties": {"title": "«Легенды Москвы","placeId": "moscow_legends","detailsUrl": "/static/places/moscow_legends.json"}}  ]}'
    ddd={"type": "FeatureCollection", "features":
            [{"type": "Feature",
              "geometry": {
                  "type": "Point",
                  "coordinates": [37.62, 55.793676]
              },
              "properties": {
                  "title": "«Легенды Москвы",
                  "placeId": "moscow_legends",
                  "detailsUrl": "/static/places/moscow_legends.json"
              }
             }
            ]}
    print('blank')
    places = Place.objects.all()
    content = {'geodict': make_geodict(places)}
    # xxx=json.dumps(ddd,ensure_ascii=False)
    # content = {'geojson': xxx}

    print('content==',content)
    return render(request, 'places/pindex.html', content)



def detail_json(request, idfromurl):
    print('--->detail_json---')
    p = get_object_or_404(Place, pk=idfromurl)
    print(p.title)
    d=p.get_place_json()
    print(d)
#     TODO json
    return HttpResponse(d, content_type='application/json')
    # return HttpResponse(d, mimetype='application/json')
    # return HttpResponse(json.dumps(dat), content_type='application/javascript')
