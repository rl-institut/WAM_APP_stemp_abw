# Generated by Django 2.1.3 on 2019-06-16 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0036_regmundemelenergydeltaresult_regmundemelenergypercapitadeltaresult_regmunenergyreeldemsharedeltaresu'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultLayerModel',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('stemp_abw.regmun',),
        ),
    ]