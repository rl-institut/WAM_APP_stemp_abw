# Generated by Django 2.1.1 on 2018-09-20 08:12

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0007_auto_20180920_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='osmpowergen',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=3035),
        ),
    ]