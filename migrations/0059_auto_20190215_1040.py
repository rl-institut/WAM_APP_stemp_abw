# Generated by Django 2.1.3 on 2019-02-15 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0058_auto_20190215_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='mundata',
            name='gen_capacity_storage',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='mundata',
            name='gen_count_storage',
            field=models.FloatField(null=True),
        ),
    ]