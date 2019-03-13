# Generated by Django 2.1.3 on 2019-03-13 12:47

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0006_auto_20190313_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScenarioData',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('data_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='data',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='data_uuid',
        ),
    ]
