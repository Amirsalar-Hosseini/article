import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinLengthValidator
from django.utils import timezone
from .managers import UserManager

class User(AbstractBaseUser):
    '''
    User model
    '''
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True, help_text='09*********')
    profile = models.ImageField(upload_to='profile/', blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    about_me = models.TextField(blank=True, null=True, help_text='optional')
    country = models.CharField(max_length=50, blank=True, help_text='optional')
    birth_date = models.DateField(null=True, blank=True, help_text='optional')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'age']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.code}'

    def is_valid(self):
        expiration_time = self.created_at + timezone.timedelta(minutes=2)
        return timezone.now() <= expiration_time and not self.is_used

    @staticmethod
    def generate_code():
        return '{:04d}'.format(random.randint(0, 9999))
