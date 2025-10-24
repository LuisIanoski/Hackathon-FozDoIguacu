from rest_framework import serializers
from .models import User, AgencyProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('usuario_id', 'username', 'email', 'is_agency')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class AgencyProfileSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = AgencyProfile
        fields = ['id', 'user', 'user_details', 'user_id', 'registration_number', 
                 'verified', 'nome_agencia', 'cnpj', 'telefone', 'descricao']
        extra_kwargs = {
            'user': {'read_only': True},
            'registration_number': {'required': False},
            'verified': {'read_only': True}
        }