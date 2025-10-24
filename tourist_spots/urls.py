from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tourist-spots', views.TouristSpotViewSet)
router.register(r'keys', views.KeyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]