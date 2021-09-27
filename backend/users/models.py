from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=150
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=100
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=254
    )
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email
