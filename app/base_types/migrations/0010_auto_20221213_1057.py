# Generated by Django 3.2.16 on 2022-12-13 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_types', '0009_auto_20221212_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='logicnodestypes',
            name='explanation',
            field=models.TextField(blank=True, max_length=2048, verbose_name='Пояснение'),
        ),
        migrations.DeleteModel(
            name='LNobjConnections',
        ),
    ]
