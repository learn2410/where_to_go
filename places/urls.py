from django.urls import path

from . import views

app_name = 'places'
urlpatterns = [
    path('', views.view_blank),
    #    path('jsn/place_<int:idfromurl>',views.detail_json,name='json_place')
    path('<int:idfromurl>', views.detail_json, name='json_place')

]
