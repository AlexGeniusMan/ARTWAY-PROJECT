from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image


class Artifact(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    img = models.ImageField(_("Фотография"), null=True, upload_to='artifacts/photos', blank=True)
    audio = models.FileField(_("Аудио"), upload_to='artifacts/audios', blank=True)
    description = models.TextField(_("Описание"), max_length=10000, blank=True)

    qr_code = models.ImageField(_('QR code'), upload_to='artifacts/qrs', blank=True)

    prev = models.IntegerField(_("Экспонат выше"), null=True, blank=True)

    hall = models.ForeignKey('Hall', on_delete=models.PROTECT, verbose_name='Зал',
                             related_name='artifacts', null=True)

    class Meta:
        verbose_name = 'Экспонат'
        verbose_name_plural = 'Экспонаты'

    def __str__(self):
        # return self.name
        return str(self.id)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     print(self.img_1)
    #     im1 = Image.open(self.img_1)
    #     fname = f'{self.id}-mini.jpeg'
    #     print(fname)
    #     im1.save('media/Products/' + fname, "JPEG", quality=10)
    #     self.img_mini = 'Products/' + fname
    #     print(self.img_mini)
    #     super().save(*args, **kwargs)


class Hall(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    img = models.ImageField(_("Фотография"), null=True, upload_to='halls', blank=True)
    description = models.TextField(_("Описание"), max_length=10000, blank=True)

    prev = models.IntegerField(_("Зал выше"), null=True, blank=True)

    location = models.ForeignKey('Location', on_delete=models.PROTECT, verbose_name='Локация',
                                 related_name='halls', null=True)

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'

    def __str__(self):
        # return self.name
        return str(self.id)


class Location(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    img = models.ImageField(_("Фотография"), null=True, upload_to='locations', blank=True)
    description = models.TextField(_("Описание"), max_length=10000, blank=True)

    prev = models.IntegerField(_("Локация выше"), null=True, blank=True)

    museum = models.ForeignKey('Museum', on_delete=models.PROTECT, verbose_name='Музей',
                               related_name='locations', null=True)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        # return self.name
        return str(self.id)


class Museum(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    img = models.ImageField(_("Фотография"), null=True, upload_to='museums', blank=True)
    description = models.TextField(_("Описание"), max_length=10000, blank=True)

    class Meta:
        verbose_name = 'Музей'
        verbose_name_plural = 'Музеи'

    def __str__(self):
        # return self.name
        return str(self.id)


class User(AbstractUser):
    ROLES = (
        ('service_super_admin', 'Супер-админ сервиса'),
        ('museum_super_admin', 'Супер-админ музея'),
        ('museum_admin', 'Админ музея'),
        ('museum_cashier', 'Кассир музея'),
    )
    last_name = models.CharField(_("Фамилия"), max_length=50)
    first_name = models.CharField(_("Имя"), max_length=50)
    middle_name = models.CharField(_("Отчество"), max_length=50, blank=True)

    # role = models.CharField(_("Роль"), choices=ROLES, max_length=64, default='none', blank=True)

    museum = models.ForeignKey('Museum', on_delete=models.SET_NULL, verbose_name='Музей',
                               related_name='admins', null=True)

    REQUIRED_FIELDS = ['email', 'last_name', 'first_name', 'middle_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'
