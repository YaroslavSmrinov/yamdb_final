from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import ADMIN, CHOICES, MODERATOR, USER
from .validators import validate_me


class YamDBUserManager(UserManager):
    def create_superuser(
        self, username, email=None, password=None, **extra_fields
    ):
        user = super().create_superuser(
            username, email, password, **extra_fields
        )
        user.role = ADMIN
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    objects = YamDBUserManager()
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=CHOICES,
        default=USER,
    )
    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer.'
            + ' Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator, validate_me],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    @property
    def groups(self):
        pass

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
