# Generated by Django 2.1.3 on 2019-02-15 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0062_auto_20190215_2228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demand',
            name='ags',
        ),
        migrations.DeleteModel(
            name='Demand',
        ),
    ]
