# Generated by Django 2.1.3 on 2019-02-15 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0059_auto_20190215_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('demand_power_hh', models.FloatField()),
                ('demand_power_rca', models.FloatField()),
                ('demand_power_ind', models.FloatField()),
                ('demand_heat_hh', models.FloatField()),
                ('demand_heat_rca', models.FloatField()),
                ('demand_heat_ind', models.FloatField()),
                ('ags', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='stemp_abw.RegMun')),
            ],
        ),
        migrations.AlterField(
            model_name='mundata',
            name='pop_2011',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='mundata',
            name='pop_2017',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='mundata',
            name='pop_2030',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='mundata',
            name='pop_2050',
            field=models.IntegerField(null=True),
        ),
    ]
