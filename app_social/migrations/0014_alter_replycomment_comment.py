# Generated by Django 4.2.5 on 2023-10-26 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_social', '0013_remove_grouppost_comments_alter_comment_post_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replycomment',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='app_social.comment'),
        ),
    ]
