# Generated by Django 2.1 on 2021-02-17 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blood_pressure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=100)),
                ('systolic', models.FloatField(default=0, max_length=3, null=True)),
                ('diastolic', models.FloatField(default=0, max_length=3, null=True)),
                ('pulse', models.CharField(default=0, max_length=3, null=True)),
                ('recorded_at', models.DateTimeField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
