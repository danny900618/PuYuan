# Generated by Django 2.1 on 2021-02-14 08:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20210208_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug_information',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
