# Generated by Django 2.1.3 on 2019-06-24 08:35

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0041_auto_20190617_1821'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegSurfaceWater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
