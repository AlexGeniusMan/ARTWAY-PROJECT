# Generated by Django 3.1.2 on 2021-01-18 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_remove_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='museum',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admins', to='main_app.museum', verbose_name='Музей'),
        ),
    ]
