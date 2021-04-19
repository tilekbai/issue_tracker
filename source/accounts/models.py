from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    github = models.CharField(max_length=55, null=True, blank=True, verbose_name='Github')
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Аватар')
    about_me = models.TextField(null=True, blank=True, verbose_name='About me')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'