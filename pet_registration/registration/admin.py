from django.contrib import admin

# Register your models here.
from .models import Owner, Pet, PetWeight

admin.site.register(Owner)
admin.site.register(Pet)
admin.site.register(PetWeight)