# Generated by Django 2.1 on 2021-04-09 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('body', '0013_auto_20210326_0559'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diary_diet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=100)),
                ('description', models.CharField(blank=True, default=0, max_length=5, null=True)),
                ('meal', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=5, null=True)),
                ('tag', models.CharField(blank=True, max_length=100)),
                ('image', models.ImageField(blank=True, upload_to='diet/diet_%Y-%m-%d_%H:%M:%S')),
                ('image_count', models.IntegerField(blank=True, default=0)),
                ('lat', models.FloatField(blank=True, max_length=100)),
                ('lng', models.FloatField(blank=True, max_length=100)),
                ('recorded_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]