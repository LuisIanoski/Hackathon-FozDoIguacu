from rest_framework import serializers
from .models import TouristSpot, Key
from place_locations.serializers import LocationSerializer

class TouristSpotSerializer(serializers.ModelSerializer):
    location_details = LocationSerializer(source='location', read_only=True)

    class Meta:
        model = TouristSpot
        fields = ['id', 'nome', 'location', 'location_details', 'created_at', 'descricao', 'is_active']

class KeySerializer(serializers.ModelSerializer):
    tourist_spot = TouristSpotSerializer(read_only=True)
    tourist_spot_id = serializers.IntegerField(write_only=True)
    agency_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Key
        fields = ['id', 'tourist_spot', 'tourist_spot_id', 'agency', 'agency_id', 'key', 'code', 'created_at', 'is_active']