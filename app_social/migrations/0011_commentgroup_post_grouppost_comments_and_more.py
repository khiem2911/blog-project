# Generated by Django 4.2.5 on 2023-10-25 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_social', '0010_alter_commentgroup_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentgroup',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_social.grouppost'),
        ),
        migrations.AddField(
            model_name='grouppost',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='group_posts', to='app_social.comment'),
        ),
        migrations.AlterField(
            model_name='commentgroup',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_social.group'),
        ),
    ]
