# Generated by Django 2.2.23 on 2021-06-02 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='queue',
            name='group',
        ),
        migrations.RemoveField(
            model_name='queue',
            name='users',
        ),
        migrations.RemoveField(
            model_name='user',
            name='cur_queue',
        ),
        migrations.RemoveField(
            model_name='user',
            name='group',
        ),
        migrations.RemoveField(
            model_name='user',
            name='tmp_queue',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='Queue',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
