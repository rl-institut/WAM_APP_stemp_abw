# Generated by Django 2.1.3 on 2019-06-05 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0024_regmungencapredensityresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegMunGenCountWindDensityResult',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('stemp_abw.regmun',),
        ),
    ]
