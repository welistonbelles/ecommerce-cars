from django.urls import path
from .views import IndexView, StockView, StockViewSet, BrandViewSet, CarModelViewSet, CategoryViewSet, ColorViewSet

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('estoque/', StockView.as_view(), name='estoque'),
    path('api/v1/', StockViewSet.as_view({
        'get': 'list',
    })),
    path('api/v1/brands/', BrandViewSet.as_view({
        'get': 'list',
    })),
    path('api/v1/models/', CarModelViewSet.as_view({
        'get': 'list',
    })),
    path('api/v1/categorys/', CategoryViewSet.as_view({
        'get': 'list',
    })),
    path('api/v1/colors/', ColorViewSet.as_view({
        'get': 'list',
    })),
]