from django.shortcuts import render
from django.http import HttpResponse

from .models import Owner, Pet, PetWeight


def index(request):
    context = {"owners_list": Owner.objects.all()}
    return render(request, "registration/index.html", context)
