# Generated by Django 2.1.1 on 2018-10-10 06:41

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0037_auto_20181010_0041'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegPrioAreaWEC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
                ('bezeich_2', models.CharField(max_length=254, null=True)),
                ('bezeich_3', models.CharField(max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]