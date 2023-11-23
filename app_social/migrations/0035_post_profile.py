# Generated by Django 4.2.5 on 2023-11-21 01:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_social', '0034_chatmodel_customuser_online_status_chatnotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
    ]