from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from utils.codes import RandomPassword


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        # print "email ",email
        user.username = username
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        # user.username = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    DEVICE_TYPE = (
        ('android', 'Android'),
        ('ios', 'IOS')
    )

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True) 
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    personal_id = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        _('Staff Status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.')
    )
    is_active = models.BooleanField(
        _('Active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True,
                                   editable=False)
    modified = models.DateTimeField(
        _('Modified Date'), auto_now=True, editable=False)
    code = models.TextField(_('Code Verify'), null=True, blank=True)
    avatar = models.ImageField(max_length=1000, null=True, blank=True, upload_to="avatar")
    anonymously = models.BooleanField(
        _('Anonymous User'),
        default=False
    )
    device_unique = models.CharField(max_length=255, null=True, blank=True)
    # device_type = models.CharField(max_length=255, choices=DEVICE_TYPE, null=True, blank=True)
    is_new_register = models.BooleanField(default=True)
    flag_notification = models.BooleanField(default=True)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def secure_code(self):
        rand = RandomPassword()
        code = rand.get(max_value=settings.CODE_LEN)
        self.code = code
        self.save()
        return code

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return super(User, self).has_perm(perm, obj)

    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     print "Check Permistion ",self.is_active, self.is_superuser
    #     return super(User, self).has_module_perms(app_label)

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_superuser
