# Generated by Django 2.1.1 on 2018-09-20 09:06

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0014_rpabwbound'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rpabwbound',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiLineStringField(null=True, srid=3035),
        ),
    ]