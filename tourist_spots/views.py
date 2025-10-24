from rest_framework import viewsets, permissions
from .models import TouristSpot, Key
from .serializers import TouristSpotSerializer, KeySerializer

class TouristSpotViewSet(viewsets.ModelViewSet):
    queryset = TouristSpot.objects.all()
    serializer_class = TouristSpotSerializer
    permission_classes = [permissions.IsAuthenticated]

class KeyViewSet(viewsets.ModelViewSet):
    queryset = Key.objects.all()
    serializer_class = KeySerializer
    permission_classes = [permissions.IsAuthenticated]
