# Generated by Django 2.2.23 on 2021-06-04 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20210604_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cur_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cur_users', to='backend.Group', verbose_name='Текушая группа'),
        ),
    ]