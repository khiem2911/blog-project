# Generated by Django 4.2.5 on 2023-11-22 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_social', '0037_post_fanpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='post_fanpage',
            name='fanpage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_social.fanpage'),
        ),
    ]