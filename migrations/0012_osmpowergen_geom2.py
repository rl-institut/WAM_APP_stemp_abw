# Generated by Django 2.1.1 on 2018-09-20 08:42

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0011_auto_20180920_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='osmpowergen',
            name='geom2',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=3035),
        ),
    ]
