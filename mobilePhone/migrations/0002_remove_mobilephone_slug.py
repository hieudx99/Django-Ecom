# Generated by Django 4.0.4 on 2022-05-02 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mobilePhone', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobilephone',
            name='slug',
        ),
    ]