from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
import qrcode
# from io import BytesIO
# from django.core.files import File
from PIL import Image


class Ticket(models.Model):
    token = models.CharField(_("Токен"), max_length=30)
    created_at = models.DateTimeField(_("Время создания"), default=timezone.now)
    pdf = models.FileField(_("PDF"), upload_to='tickets', blank=True)

    museum = models.ForeignKey('Museum', on_delete=models.CASCADE, verbose_name='Музей',
                               related_name='tickets', null=True)

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'

    def __str__(self):
        return f'Билет №{self.id}'


class Artifact(models.Model):
    name = models.CharField(_("Название"), max_length=100)

    img_1 = models.ImageField(_("Фотография #1"), null=True, upload_to='artifacts/photos', blank=True)
    img_2 = models.ImageField(_("Фотография #2"), null=True, upload_to='artifacts/photos', blank=True)
    img_3 = models.ImageField(_("Фотография #3"), null=True, upload_to='artifacts/photos', blank=True)
    img_4 = models.ImageField(_("Фотография #4"), null=True, upload_to='artifacts/photos', blank=True)
    img_5 = models.ImageField(_("Фотография #5"), null=True, upload_to='artifacts/photos', blank=True)

    audio_1 = models.FileField(_("Аудио #1"), upload_to='artifacts/audios', blank=True)
    audio_2 = models.FileField(_("Аудио #2"), upload_to='artifacts/audios', blank=True)
    audio_3 = models.FileField(_("Аудио #3"), upload_to='artifacts/audios', blank=True)
    audio_4 = models.FileField(_("Аудио #4"), upload_to='artifacts/audios', blank=True)
    audio_5 = models.FileField(_("Аудио #5"), upload_to='artifacts/audios', blank=True)

    video = models.CharField(_("Ссылка на видео"), max_length=1000, blank=True)

    description = models.TextField(_("Описание"), max_length=10000, blank=True)

    qr_code = models.ImageField(_('QR code'), upload_to='artifacts/qrs', blank=True)

    prev = models.IntegerField(_("Экспонат выше"), null=True, blank=True)

    hall = models.ForeignKey('Hall', on_delete=models.CASCADE, verbose_name='Зал',
                             related_name='artifacts', null=True)

    class Meta:
        verbose_name = 'Экспонат'
        verbose_name_plural = 'Экспонаты'

    def __str__(self):
        return f'{self.name} ({self.id})'

    @classmethod
    def create(cls, name, description, hall, prev,
               img_1,
               img_2,
               img_3,
               img_4,
               img_5,
               audio_1,
               audio_2,
               audio_3,
               audio_4,
               audio_5,
               video,
               ):
        artifact = cls(name=name, description=description, hall=hall, prev=prev,
                       img_1=img_1,
                       img_2=img_2,
                       img_3=img_3,
                       img_4=img_4,
                       img_5=img_5,
                       audio_1=audio_1,
                       audio_2=audio_2,
                       audio_3=audio_3,
                       audio_4=audio_4,
                       audio_5=audio_5,
                       video=video
                       )
        return artifact

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        qr = qrcode.QRCode(version=1, box_size=15, border=2)
        qr.add_data('https://devgang.ru/artifacts/' + str(self.id))
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        canvas = Image.new('RGB', (500, 500), 'white')
        canvas.paste(img)
        fname = f'qr_{self.id}.jpeg'
        # buffer = BytesIO()
        canvas.save('media/artifacts/qrs/' + fname, 'jpeg')
        canvas.close()
        self.qr_code = 'artifacts/qrs/' + fname
        # self.qr_code.save(fname, File(buffer), save=False)
        super().save(*args, **kwargs)

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


# class ArtifactLink(models.Model):
#     name = models.CharField(_("Название ссылки"), max_length=50)
#     link = models.CharField(_("Ссылка"), max_length=1000)
#     artifact = models.ForeignKey('Artifact', on_delete=models.CASCADE, verbose_name='Экспонат',
#                                  related_name='links', null=True, blank=True)
#
#     class Meta:
#         verbose_name = 'Ссылка'
#         verbose_name_plural = 'Ссылки'


class Hall(models.Model):
    name = models.CharField(_("Название"), max_length=100)

    prev = models.IntegerField(_("Зал выше"), null=True, blank=True)

    location = models.ForeignKey('Location', on_delete=models.CASCADE, verbose_name='Локация',
                                 related_name='halls', null=True)

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'

    def __str__(self):
        return f'{self.name} ({self.id})'


class Location(models.Model):
    name = models.CharField(_("Название"), max_length=100)

    prev = models.IntegerField(_("Локация выше"), null=True, blank=True)

    museum = models.ForeignKey('Museum', on_delete=models.CASCADE, verbose_name='Музей',
                               related_name='locations', null=True)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return f'{self.name} ({self.id})'


class Museum(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    img = models.ImageField(_("Фотография"), null=True, upload_to='museums', blank=True)
    description = models.TextField(_("Описание"), max_length=10000, blank=True)
    ticket_lifetime = models.IntegerField(_("Время действия билета"), default=3)

    class Meta:
        verbose_name = 'Музей'
        verbose_name_plural = 'Музеи'

    def __str__(self):
        return self.name


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

    museum = models.ForeignKey('Museum', on_delete=models.CASCADE, verbose_name='Музей',
                               related_name='admins', null=True, blank=True)

    REQUIRED_FIELDS = ['email', 'last_name', 'first_name', 'middle_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'
