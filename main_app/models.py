from django.utils.translation import gettext_lazy as _
from django.db import models


class Artifact(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    img = models.ImageField(_("Фотография"), null=True, upload_to='Artifact photos', blank=True)
    audio = models.FileField(_("Аудио"), upload_to='Artifact audios', blank=True)
    description = models.TextField(_("Описание"), max_length=10000, blank=True)

    class Meta:
        verbose_name = 'Экспонат'
        verbose_name_plural = 'Экспонаты'

    def __str__(self):
        return self.name
