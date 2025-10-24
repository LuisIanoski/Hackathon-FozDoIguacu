from rest_framework import viewsets, permissions
from .models import User, AgencyProfile
from .serializers import UserSerializer, AgencyProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class AgencyProfileViewSet(viewsets.ModelViewSet):
    queryset = AgencyProfile.objects.all()
    serializer_class = AgencyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
