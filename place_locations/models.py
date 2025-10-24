from django.db import models
from django.core.validators import MinLengthValidator

class AbstractLocation(models.Model):
    """
    Modelo base abstrato para localização
    """
    numero = models.IntegerField()
    rua = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255, db_index=True)
    estado = models.CharField(max_length=2)
    pais = models.CharField(max_length=255, default='Brasil')
    cep = models.CharField(max_length=8, validators=[MinLengthValidator(8)])

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}"

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['cidade', 'estado']),
            models.Index(fields=['cep']),
        ]

class Location(AbstractLocation):
    """
    Modelo concreto de localização com metadados adicionais
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'location'
