# Generated by Django 2.1 on 2021-02-14 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20210214_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug_information',
            name='Type',
            field=models.CharField(default=0, max_length=1),
        ),
    ]
