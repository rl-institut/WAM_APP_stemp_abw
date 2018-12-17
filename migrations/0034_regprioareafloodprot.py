# Generated by Django 2.1.1 on 2018-10-09 15:49

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0033_regresidareab500'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegPrioAreaFloodProt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
                ('bemerkunge', models.CharField(max_length=254, null=True)),
                ('bezeich_2', models.CharField(max_length=254, null=True)),
                ('bezeich_3', models.CharField(max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]