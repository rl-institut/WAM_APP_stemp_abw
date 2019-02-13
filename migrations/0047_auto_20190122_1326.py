# Generated by Django 2.1.3 on 2019-01-22 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0046_regbioreserve_regffhprotareab_reginfrasaviation_reginfrashvgrid_reginfrasrailway_reginfrasroad_regla'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegMunPopDensity',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('stemp_abw.regmun',),
        ),
        migrations.AddField(
            model_name='regmun',
            name='pop_km2',
            field=models.FloatField(null=True),
        ),
    ]