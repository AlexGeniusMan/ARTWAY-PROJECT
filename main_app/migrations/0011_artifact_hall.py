# Generated by Django 3.1.2 on 2021-01-17 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_auto_20210117_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='artifact',
            name='hall',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='artifacts', to='main_app.hall', verbose_name='Зал'),
        ),
    ]
