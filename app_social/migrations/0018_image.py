# Generated by Django 4.2.6 on 2023-10-30 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_social', '0017_friendrequest_rejected'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]
