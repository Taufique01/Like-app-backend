# Generated by Django 2.2.7 on 2019-11-15 22:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('google_social_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesstoken',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='access_token', to=settings.AUTH_USER_MODEL),
        ),
    ]
