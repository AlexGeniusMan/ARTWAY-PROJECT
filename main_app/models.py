from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image


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
        return self.name


class Museum(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    img = models.ImageField(_("Фотография"), null=True, upload_to='museums', blank=True)
    description = models.TextField(_("Описание"), max_length=10000, blank=True)

    class Meta:
        verbose_name = 'Музей'
        verbose_name_plural = 'Музеи'

    def __str__(self):
        return self.name


class Artifact(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    img = models.ImageField(_("Фотография"), null=True, upload_to='artifact_photos', blank=True)
    audio = models.FileField(_("Аудио"), upload_to='artifact_audios', blank=True)
    description = models.TextField(_("Описание"), max_length=10000, blank=True)

    prev = models.IntegerField(_("Экспонат выше"), null=True, blank=True)

    qr_code = models.ImageField(_('QR code'), upload_to='artifact_qrs', blank=True)

    class Meta:
        verbose_name = 'Экспонат'
        verbose_name_plural = 'Экспонаты'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(version=1, box_size=15, border=2)
        qr.add_data('https://devgang.ru/artifacts/' + str(self.id))
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        canvas = Image.new('RGB', (500, 500), 'white')
        canvas.paste(img)
        fname = f'qr_code-{self.id}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


class User(AbstractUser):
    last_name = models.CharField(_("Фамилия"), max_length=50)
    first_name = models.CharField(_("Имя"), max_length=50)
    middle_name = models.CharField(_("Отчество"), max_length=50)

    museum = models.ForeignKey('Museum', on_delete=models.SET_NULL, verbose_name='Музей',
                               related_name='admins', null=True)

    REQUIRED_FIELDS = ['email', 'last_name', 'first_name', 'middle_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'
