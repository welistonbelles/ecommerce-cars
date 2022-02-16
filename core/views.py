from statistics import mode
from unicodedata import category
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Car, Brand, CarModel
from .serializers import CarSerializer, BrandSerializer, CarModelSerializer

# DRF
from rest_framework import viewsets, status
from rest_framework.response import Response


# Create your views here.
class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['init_cars'] = Car.objects.all()[:4]
        context['middle_cars'] = Car.objects.all()[4:8]
        context['end_cars'] = Car.objects.all()[8:12]
        return self.render_to_response(context)

class StockView(TemplateView):
    template_name = 'core/estoque.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.all().order_by('id')
    serializer_class = CarSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.query_params.get('order'):
            if request.query_params['order'].lower() == 'asc':
                queryset = Car.objects.all().order_by('price')
            elif request.query_params['order'].lower() == 'desc':
                queryset = Car.objects.all().order_by('-price')
        
        if request.query_params.get('state'):
            try:
                if request.query_params['state'].lower() == 'new':
                    queryset = queryset.filter(kms=0)
                elif request.query_params['state'].lower() == 'used':
                    queryset = queryset.filter(kms__gte=1)
            except Exception as error:
                pass

        if request.query_params.get('brand'):
            try:
                brand = Brand.objects.filter(brand=request.query_params['brand'])
                queryset = queryset.filter(brand=brand.first().id)
            except Exception as error:
                pass

        if request.query_params.get('model'):
            try:
                model = CarModel.objects.filter(model=request.query_params['model'])
                queryset = queryset.filter(model=model.first().id)
            except Exception as error:
                pass
                
        if request.query_params.get('color'):
            try:
                queryset = queryset.filter(color=request.query_params['color'])
            except Exception as error:
                pass
        
        if request.query_params.get('year'):
            try:
                year = request.query_params['year'].split('-')
                if len(year) > 1:
                    fromYear, toYear = year
                    queryset = queryset.filter(year__gte=fromYear, year__lte=toYear)
                else:
                    fromYear = year[0]
                    queryset = queryset.filter(year__gte=fromYear)
            except Exception as error:
                pass
        
        if request.query_params.get('price'):
            try:
                price = request.query_params['price'].split('-')
                if len(price) > 1:
                    fromPrice, toPrice = price
                    queryset = queryset.filter(price__gte=fromPrice, price__lte=toPrice)
                else:
                    fromPrice = price[0]
                    queryset = queryset.filter(price__gte=fromPrice)
            except Exception as error:
                pass

        if request.query_params.get('exchange'):
            try:
                exchanges = request.query_params['exchange'].split('/')
                queryset = queryset.filter(exchange__in=exchanges)

            except Exception as error:
                pass
        
        if request.query_params.get('fuel'):
            try:
                fuel = request.query_params['fuel'].split('-')
                queryset = queryset.filter(fuel__in=fuel)

            except Exception as error:
                pass
        
        if request.query_params.get('doors'):
            try:
                doors = request.query_params['doors'].split('-')
                queryset = queryset.filter(doors__in=doors)
            except Exception as error:
                pass
        
        if request.query_params.get('category'):
            try:
                queryset = queryset.filter(category=request.query_params['category'])
            except Exception as error:
                pass

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for car in serializer.data:
                car['brand'] = Brand.objects.filter(id=car['brand']).first().brand
                car['model'] = CarModel.objects.filter(id=car['model']).first().model
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CarModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CarModel.objects.all().order_by('id')
    serializer_class = CarModelSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.query_params.get('brand'):
            try:
                brand = Brand.objects.filter(brand=request.query_params['brand'])
                queryset = queryset.filter(brand=brand.first().id)
            except:
                pass
                
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.all().order_by('id')
    serializer_class = CarSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        first = queryset.first()
        lista = [{'category': category[1]} for category in first.CATEGORY_CHOICES]
        return Response(lista)


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.all().order_by('id')
    serializer_class = CarSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        first = queryset.first()
        lista = [{'color': color[1]} for color in first.COLOR_CHOICES]
        return Response(lista)