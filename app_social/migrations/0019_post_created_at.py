# Generated by Django 4.2.6 on 2023-10-30 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_social', '0018_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
