from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import os


def user_avatar_path(instance, filename):
    # Загрузка аватаров в media/users/user_id/avatar.ext
    return f'users/{instance.id}/avatar/{filename}'


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    avatar = models.ImageField(
        _('avatar'),
        upload_to=user_avatar_path,
        blank=True,
        null=True
    )
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    bio = models.TextField(_('biography'), blank=True)

    # Отключаем неиспользуемые поля
    username = None
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Удаляем старый аватар при обновлении
        if self.pk:
            old_avatar = CustomUser.objects.get(pk=self.pk).avatar
            if old_avatar and old_avatar != self.avatar:
                old_avatar.delete(save=False)
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()