from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from place_locations.models import Location
import uuid
import string
import random
from django.core.cache import cache

class TouristSpot(models.Model):
    """
    Ponto Turístico com cache para otimização
    """
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, db_index=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='tourist_spots')
    created_at = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Limpa o cache quando o ponto turístico é atualizado
        cache_key = f'tourist_spot_{self.id}'
        cache.delete(cache_key)
        super().save(*args, **kwargs)

    @property
    def cached_keys(self):
        """
        Retorna as keys do ponto turístico com cache
        """
        cache_key = f'tourist_spot_keys_{self.id}'
        keys = cache.get(cache_key)
        if keys is None:
            keys = list(self.keys.all())
            cache.set(cache_key, keys, timeout=3600)  # Cache por 1 hora
        return keys

    class Meta:
        db_table = 'tourist_spot'
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['is_active']),
        ]

class Key(models.Model):
    """
    Chave de acesso com geração automática e validação
    """
    id = models.AutoField(primary_key=True)
    tourist_spot = models.ForeignKey(TouristSpot, on_delete=models.CASCADE, related_name='keys')
    agency = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='keys', blank=True, null=True)
    key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=8, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self._generate_unique_code()
        super().save(*args, **kwargs)
        # Limpa o cache das keys do ponto turístico
        cache.delete(f'tourist_spot_keys_{self.tourist_spot_id}')

    def _generate_unique_code(self):
        """
        Gera um código único usando um prefixo e verificando unicidade
        """
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not Key.objects.filter(code=code).exists():
                return code

    class Meta:
        db_table = 'key'
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]
