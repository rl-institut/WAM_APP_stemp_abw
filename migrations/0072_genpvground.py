# Generated by Django 2.1.3 on 2019-02-23 09:24

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0071_delete_hvmvsubst'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenPVGround',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]