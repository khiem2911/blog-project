# Generated by Django 4.2.5 on 2023-10-14 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myBlogs', '0009_rename_images_post_imagespost'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='num_likes',
            field=models.IntegerField(default=0),
        ),
    ]