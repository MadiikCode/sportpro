from django.db import models
from django.db.models import Avg  # Импортируем Avg из django.db.models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class SportCategory(models.Model):
    name = models.CharField(
        _('name'),
        max_length=100,
        help_text=_('Enter the name of the sport')
    )
    description = models.TextField(
        _('description'),
        help_text=_('Describe the sport')
    )
    image = models.ImageField(
        _('image'),
        upload_to='sports/',
        blank=True,
        null=True,
        help_text=_('Upload an image for the sport')
    )
    rules = models.TextField(
        _('rules'),
        blank=True,
        help_text=_('Enter the basic rules of the sport')
    )
    equipment = models.TextField(
        _('required equipment'),
        blank=True,
        help_text=_('List the required equipment')
    )
    popular_countries = models.CharField(
        _('popular countries'),
        max_length=255,
        blank=True,
        help_text=_('List countries where this sport is popular')
    )
    is_olympic = models.BooleanField(
        _('Olympic sport'),
        default=False,
        help_text=_('Is this an Olympic sport?')
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sports',
        verbose_name=_('author')
    )

    class Meta:
        verbose_name = _('sport category')
        verbose_name_plural = _('sport categories')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Удаляем старое изображение при обновлении
        if self.pk:
            try:
                old = SportCategory.objects.get(pk=self.pk)
                if old.image and old.image != self.image:
                    old.image.delete(save=False)
            except SportCategory.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Удаляем изображение при удалении объекта
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def average_rating(self):
        """Вычисляет средний рейтинг для этого вида спорта"""
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0


class SportReview(models.Model):
    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]

    sport = models.ForeignKey(
        SportCategory,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('sport')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    rating = models.PositiveSmallIntegerField(
        _('rating'),
        choices=RATING_CHOICES
    )
    comment = models.TextField(
        _('comment'),
        blank=True
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
        unique_together = ('sport', 'user')  # Один отзыв на пользователя
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} - {self.sport.name} ({self.get_rating_display()})'