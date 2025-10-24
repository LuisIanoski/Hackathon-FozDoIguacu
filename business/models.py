from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from place_locations.models import Location
from tourist_spots.models import Key
import string
import random
from django.core.cache import cache

class Commerce(models.Model):
    """
    Estabelecimento comercial
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, db_index=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='commerces')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'commerce'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
        ]

class Coupon(models.Model):
    """
    Cupom promocional com validação e cache
    """
    id = models.AutoField(primary_key=True)
    commerce = models.ForeignKey(Commerce, on_delete=models.CASCADE, related_name='coupons')
    key = models.ForeignKey(Key, on_delete=models.CASCADE, related_name='coupons')
    code = models.CharField(max_length=10, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(editable=False)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self._generate_unique_code()
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=1)
        super().save(*args, **kwargs)
        # Limpa o cache
        cache.delete(f'coupon_{self.code}')

    def _generate_unique_code(self):
        """
        Gera um código promocional único
        """
        while True:
            code = 'PROMO' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            if not Coupon.objects.filter(code=code).exists():
                return code

    @property
    def is_valid(self):
        """
        Verifica se o cupom é válido com cache
        """
        cache_key = f'coupon_valid_{self.code}'
        is_valid = cache.get(cache_key)
        if is_valid is None:
            is_valid = (
                not self.is_used and 
                timezone.now() <= self.expires_at
            )
            cache.set(cache_key, is_valid, timeout=300)  # Cache por 5 minutos
        return is_valid

    def use_coupon(self):
        """
        Marca o cupom como usado
        """
        if not self.is_valid:
            raise ValidationError("Cupom inválido ou já utilizado")
        self.is_used = True
        self.used_at = timezone.now()
        self.save()

    class Meta:
        db_table = 'coupon'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_used']),
            models.Index(fields=['expires_at']),
        ]
