# Generated by Django 2.1 on 2021-02-24 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('body', '0005_auto_20210224_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weight',
            name='recorded_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
