from django.urls import path

from . import views

app_name = 'places'
urlpatterns = [
    path('', views.view_blank),
    path('<int:place_id>', views.detail_json, name='json_place')

]
