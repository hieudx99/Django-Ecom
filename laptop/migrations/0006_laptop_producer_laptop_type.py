# Generated by Django 4.0.4 on 2022-04-27 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('laptop', '0005_alter_type_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptop',
            name='producer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='laptop.producer'),
        ),
        migrations.AddField(
            model_name='laptop',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='laptop.type'),
        ),
    ]
