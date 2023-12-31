# Generated by Django 4.2.5 on 2023-11-01 01:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_social', '0022_alter_follow_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='liked',
            field=models.TextField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('follower', 'following')},
        ),
    ]
