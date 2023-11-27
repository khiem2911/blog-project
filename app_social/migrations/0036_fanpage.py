# Generated by Django 4.2.5 on 2023-11-21 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_social', '0035_post_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fanpage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('imgFanpage', models.ImageField(blank=True, null=True, upload_to='fanpage/')),
                ('imgFanpageCover', models.ImageField(blank=True, null=True, upload_to='fanpageCover/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
