# Generated by Django 4.2.5 on 2023-10-13 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myBlogs', '0008_alter_post_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='images',
            new_name='imagespost',
        ),
    ]
