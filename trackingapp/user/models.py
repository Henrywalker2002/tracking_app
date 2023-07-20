import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db import transaction
from functools import reduce
from django.utils import timezone
from datetime import timedelta


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=128)
    password = models.CharField(max_length=128, null=False)
    first_name = models.CharField(max_length=128, null=False)
    last_name = models.CharField(max_length=128, null=False)
    phone = models.CharField(max_length=128, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    roles = models.ManyToManyField(to="permissions.Role")

    USERNAME_FIELD = 'email'
    objects = BaseUserManager()

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def role_names(self):
        user = User.objects.filter(id=self.id).first()
        return list(user.roles.all().values_list('friendly_name', flat=True))

    def __str__(self):
        return self.email


class ResetCodeUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=128)
    code = models.CharField(max_length=6)
    expired_time = models.DateTimeField(
        default=timezone.now() + timedelta(days=1))
