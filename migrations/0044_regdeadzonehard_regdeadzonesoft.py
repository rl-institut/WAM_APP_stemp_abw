# Generated by Django 2.1.1 on 2018-10-10 09:36

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0043_regresidareab1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegDeadZoneHard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegDeadZoneSoft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
