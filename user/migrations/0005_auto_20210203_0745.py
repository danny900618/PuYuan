# Generated by Django 2.1 on 2021-02-03 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210203_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medical_information',
            name='disabetes_type',
            field=models.IntegerField(blank=True, default=True),
        ),
    ]
