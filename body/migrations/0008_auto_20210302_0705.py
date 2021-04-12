# Generated by Django 2.1 on 2021-03-02 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('body', '0007_blood_sugar'),
    ]

    operations = [
        migrations.AddField(
            model_name='blood_pressure',
            name='user_id',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='blood_sugar',
            name='user_id',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='weight',
            name='user_id',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True),
        ),
    ]
