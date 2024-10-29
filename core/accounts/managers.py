from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    '''
    management user model
    '''

    def create_user(self, first_name, last_name, email, phone_number, password=None, **extra_fields):
        if not first_name:
            raise ValueError('First name is required')

        if not last_name:
            raise ValueError('Last name is required')

        if not email:
            raise ValueError('Email is required')

        if not phone_number:
            raise ValueError('Phone number is required')

        user = self.model(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, phone_number, password):
        user = self.create_user(first_name, last_name, email, phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user