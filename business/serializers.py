from rest_framework import serializers
from .models import Commerce, Coupon
from place_locations.serializers import LocationSerializer
from tourist_spots.serializers import KeySerializer

class CommerceSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    location_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Commerce
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    commerce = CommerceSerializer(read_only=True)
    key = KeySerializer(read_only=True)
    commerce_id = serializers.IntegerField(write_only=True)
    key_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Coupon
        fields = '__all__'