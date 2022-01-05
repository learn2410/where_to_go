from django.shortcuts import render


# Create your views here.
def view_blank(request):
    return render(request, 'places/places_blank.html')
