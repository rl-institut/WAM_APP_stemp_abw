# Generated by Django 2.1.1 on 2018-10-09 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0024_auto_20181009_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regprioareares',
            name='bezeich_2',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='regprioareares',
            name='bezeich_3',
            field=models.CharField(max_length=254, null=True),
        ),
    ]