from django.contrib.auth.models import User
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils.translation import gettext_lazy as _


class Family(MPTTModel):
    members = models.ManyToManyField(
        User,
        through='FamilyMember',
        related_name='families',
        verbose_name=_("Члены семьи")
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subfamilies',
        verbose_name=_("Семейная связь")
    )

    name = models.CharField(max_length=255, verbose_name=_("Имя"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))
    preview = models.ImageField(upload_to='family_preview/', blank=True, null=True, verbose_name=_("Фотография семьи"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _("Семья")
        verbose_name_plural = _("Семьи")


class FamilyMember(models.Model):
    ROLE_CHOICES = [
        ('son', 'Сын'),
        ('daughter', 'Дочь'),
        ('father', 'Отец'),
        ('mother', 'Мать'),
        ('grandmother', 'Бабушка'),
        ('grandfather', 'Дедушка'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Пользователь"),
                             related_name='family_members')
    family = models.ForeignKey(Family, on_delete=models.CASCADE, verbose_name=_("Семья"),
                               related_name='family_members')
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, verbose_name=_("Роль"))

    def __str__(self):
        return f"Роль {self.user} в семье {self.family}: {self.role}"

    class Meta:
        verbose_name = _("Член семьи")
        verbose_name_plural = _("Члены семьи")


class FamilyImage(models.Model):
    family = models.ForeignKey(Family, related_name='images', on_delete=models.CASCADE, verbose_name=_("Семья"))
    image = models.ImageField(upload_to='family_images/', verbose_name=_("Изображение"))

    def __str__(self):
        return f"Изображение для {self.family.name}"

    class Meta:
        verbose_name = _("Изображение семьи")
        verbose_name_plural = _("Изображения семей")
