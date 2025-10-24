from rest_framework import viewsets, permissions
from .models import Commerce, Coupon
from .serializers import CommerceSerializer, CouponSerializer

class CommerceViewSet(viewsets.ModelViewSet):
    queryset = Commerce.objects.all()
    serializer_class = CommerceSerializer
    permission_classes = [permissions.IsAuthenticated]

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]
