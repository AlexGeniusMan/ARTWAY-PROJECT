# Generated by Django 3.1.2 on 2021-01-17 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_hall'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artifact',
            name='audio',
            field=models.FileField(blank=True, upload_to='artifacts/audios', verbose_name='Аудио'),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='artifacts/photos', verbose_name='Фотография'),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='artifacts/qrs', verbose_name='QR code'),
        ),
    ]
