# Generated by Django 2.2.23 on 2021-06-04 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20210604_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cur_queue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cur_users', to='backend.Queue', verbose_name='Текушая очередь'),
        ),
    ]
