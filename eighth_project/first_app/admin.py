from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Brand, Car

admin.site.register(Brand)
admin.site.register(Car)