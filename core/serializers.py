from rest_framework import serializers

from .models import Car, Brand, CarModel

class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = (
            'id',
            'brand',
            'model',
            'year',
            'new',
            'kms',
            'price',
            'category',
            'exchange',
            'color',
            'fuel',
            'doors',
            'image'
        )

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = (
            'id',
            'brand'
        )

class CarModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel
        fields = (
            'id',
            'brand',
            'model',
        )