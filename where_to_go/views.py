from django.http import HttpResponse
from django.shortcuts import render

def view_tmp(request):
    return render(request,'index.html')
