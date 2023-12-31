# Generated by Django 4.2.5 on 2023-11-11 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_social', '0029_customuser_imgcover'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.ManyToManyField(blank=True, to='app_social.video'),
        ),
    ]
