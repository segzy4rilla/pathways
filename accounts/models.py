from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first_name'), max_length=200)
    last_name = models.CharField(_('last_name'), max_length=200)
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()

    def get_first_name(self):
        """
        Return the first name
        """
        return self.first_name

    def get_fullname(self):
        """
        Return the fullname
        :return: fullname
        """
        fullname = '{} {}'.format(self.first_name, self.last_name)
        return fullname

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to this user
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    clinic_name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'

    def __str__(self):
        return self.clinic_name


class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='staffs')

    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staffs'

    def __str__(self):
        return self.user.get_fullname
