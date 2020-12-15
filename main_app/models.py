from django.utils.translation import gettext_lazy as _
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


class Artifact(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    img = models.ImageField(_("Фотография"), null=True, upload_to='Artifact photos', blank=True)
    audio = models.FileField(_("Аудио"), upload_to='Artifact audios', blank=True)
    description = models.TextField(_("Описание"), max_length=10000, blank=True)

    qr_code = models.ImageField(_('QR code'), upload_to='Artifact QR-codes', blank=True)

    class Meta:
        verbose_name = 'Экспонат'
        verbose_name_plural = 'Экспонаты'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(version=1, box_size=15, border=2)
        qr.add_data('https://devgang.ru/artifact/' + str(self.id))
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
