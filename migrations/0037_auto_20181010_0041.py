# Generated by Django 2.1.1 on 2018-10-09 22:41

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0036_genwec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genwec',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPointField(null=True, srid=3035),
        ),
    ]
