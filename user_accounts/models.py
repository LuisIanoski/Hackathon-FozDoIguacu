from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

class User(AbstractUser):
    """
    Usuário do sistema com capacidade de ser agência
    """
    usuario_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, db_index=True)
    is_agency = models.BooleanField(default=False)

    class Meta:
        db_table = 'user'
        indexes = [
            models.Index(fields=['email']),
        ]

class AgencyProfile(models.Model):
    """
    Perfil específico para agências
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agency_profile', null=True, blank=True)
    registration_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    verified = models.BooleanField(default=False)
    nome_agencia = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14)
    telefone = models.CharField(max_length=20)
    descricao = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'agency_profile'
