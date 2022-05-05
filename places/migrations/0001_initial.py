# Generated by Django 3.2.13 on 2022-04-17 07:38

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('description_short', models.TextField(blank=True)),
                ('description_long', tinymce.models.HTMLField(blank=True)),
                ('lng', models.FloatField(verbose_name='долгота')),
                ('lat', models.FloatField(verbose_name='широта')),
            ],
            options={
                'verbose_name': 'МЕСТО',
                'verbose_name_plural': 'МЕСТА',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=0, verbose_name='номер')),
                ('img', models.ImageField(upload_to='image')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myplace', to='places.place')),
            ],
            options={
                'verbose_name': 'ФОТО',
                'verbose_name_plural': 'ФОТОГРАФИИ',
                'ordering': ['number'],
            },
        ),
    ]
