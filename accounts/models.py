from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
import string
import random
import uuid

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agency_profile')
    registration_number = models.CharField(max_length=20, unique=True)
    verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'agency_profile'