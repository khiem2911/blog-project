# Generated by Django 4.2.6 on 2023-10-27 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_social', '0014_alter_replycomment_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatar/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')], default=None, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='lives',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]