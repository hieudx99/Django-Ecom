# Generated by Django 4.0.4 on 2022-04-27 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laptop', '0002_remove_laptopitem_laptop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='laptopitem',
            name='item_ptr',
        ),
        migrations.DeleteModel(
            name='Laptop',
        ),
        migrations.DeleteModel(
            name='LaptopItem',
        ),
        migrations.DeleteModel(
            name='Producer',
        ),
        migrations.DeleteModel(
            name='Type',
        ),
    ]
