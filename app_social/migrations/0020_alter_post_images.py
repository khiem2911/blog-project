# Generated by Django 4.2.6 on 2023-10-30 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_social', '0019_post_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='images',
            field=models.ManyToManyField(blank=True, to='app_social.image'),
        ),
    ]
