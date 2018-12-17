# Generated by Django 2.1.1 on 2018-10-09 06:34

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0021_auto_20181009_0815'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegionWaterProtAreas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
                ('gebietsnam', models.CharField(max_length=254)),
                ('gebietsnum', models.CharField(max_length=254)),
                ('rechtsgrun', models.CharField(max_length=254)),
                ('schutzzone', models.CharField(max_length=254)),
                ('erfassungs', models.CharField(max_length=254)),
                ('amtsblatt', models.CharField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]