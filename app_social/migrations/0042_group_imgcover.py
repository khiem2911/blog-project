# Generated by Django 4.2.7 on 2023-11-24 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_social', '0041_fanpage_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='imgcover',
            field=models.ImageField(blank=True, null=True, upload_to='imgcover/'),
        ),
    ]
