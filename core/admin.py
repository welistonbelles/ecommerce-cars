from django.contrib import admin

# Register your models here.
from .models import Car, Brand, CarModel

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'brand', 'category', 'year')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand',)

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('model',)