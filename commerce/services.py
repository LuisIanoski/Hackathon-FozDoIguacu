from tourism.models import TouristSpot, Key
from commerce.models import Commerce, Coupon
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction

class CouponService:
    """
    Serviço para gerenciamento de cupons
    """
    @staticmethod
    @transaction.atomic
    def generate_coupon(key_code: str, tourist_spot_id: int, commerce_id: int) -> Coupon:
        """
        Gera um novo cupom validando todas as regras de negócio
        """
        try:
            key = Key.objects.select_related('tourist_spot').get(
                code=key_code,
                is_active=True
            )
        except Key.DoesNotExist:
            raise ValidationError("Chave inválida")

        tourist_spot = TouristSpot.objects.select_related('location').get(id=tourist_spot_id)
        commerce = Commerce.objects.select_related('location').get(id=commerce_id)

        # Validações
        if not key.tourist_spot_id == tourist_spot_id:
            raise ValidationError("Chave não pertence a este ponto turístico")

        if tourist_spot.location.cidade != commerce.location.cidade:
            raise ValidationError("Comércio deve estar na mesma cidade do ponto turístico")

        # Cria o cupom
        return Coupon.objects.create(
            commerce=commerce,
            key=key
        )

    @staticmethod
    def validate_coupon(code: str) -> bool:
        """
        Valida um cupom pelo código
        """
        try:
            coupon = Coupon.objects.get(code=code)
            return coupon.is_valid
        except Coupon.DoesNotExist:
            return False

    @staticmethod
    @transaction.atomic
    def use_coupon(code: str) -> bool:
        """
        Utiliza um cupom se ele for válido
        """
        try:
            coupon = Coupon.objects.select_for_update().get(code=code)
            coupon.use_coupon()
            return True
        except (Coupon.DoesNotExist, ValidationError):
            return False