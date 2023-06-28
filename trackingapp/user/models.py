import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from functools import reduce


class AppUser:
    id = models.UUIDField(primary_key= True)
    def __init__(self, id, email, phone, permissions, is_active):
        self.id = id
        self.email = email
        self.phone = phone
        self.permissions = permissions
        self.is_active = is_active

    class Meta:
        abstract = True


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=128)
    password = models.CharField(max_length=128, null=False)
    first_name = models.CharField(max_length=128, null=False)
    last_name = models.CharField(max_length=128, null=False)
    phone = models.CharField(max_length=128, null=False)
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    roles = models.ManyToManyField(to="permissions.Role")

    USERNAME_FIELD = 'email'
    objects = BaseUserManager()

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def permission_code_names(self):
        user = User.objects.filter(id=self.id).first()
        return reduce(lambda prev, curr: prev + list(curr.permission.all().values_list('code_name', flat=True)), user.roles.all(), [])
    
    @property
    def role_names(self):
        user = User.objects.filter(id=self.id).first()
        return list(user.roles.all().values_list('friendly_name', flat = True))

    def __str__(self):
        return self.email
