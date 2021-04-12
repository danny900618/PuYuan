# Generated by Django 2.1 on 2021-02-23 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('body', '0003_auto_20210222_0127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=100)),
                ('weight', models.FloatField(default=0, max_length=10, null=True)),
                ('body_fat', models.FloatField(default=0, max_length=10, null=True)),
                ('bmi', models.FloatField(blank=True, default=0, max_length=10)),
                ('recorded_at', models.DateTimeField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
