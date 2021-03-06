# Generated by Django 2.1.3 on 2019-02-25 10:10

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DemandTs',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('el_hh', models.FloatField(blank=True, null=True)),
                ('el_rca', models.FloatField(blank=True, null=True)),
                ('el_ind', models.FloatField(blank=True, null=True)),
                ('th_hh_efh', models.FloatField(blank=True, null=True)),
                ('th_hh_mfh', models.FloatField(blank=True, null=True)),
                ('th_hh_efh_spec', models.FloatField(blank=True, null=True)),
                ('th_hh_mfh_spec', models.FloatField(blank=True, null=True)),
                ('th_rca', models.FloatField(blank=True, null=True)),
                ('th_ind', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeedinTs',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('pv_ground', models.FloatField(blank=True, null=True)),
                ('pv_roof', models.FloatField(blank=True, null=True)),
                ('hydro', models.FloatField(blank=True, null=True)),
                ('wind_sq', models.FloatField(blank=True, null=True)),
                ('wind_fs', models.FloatField(blank=True, null=True)),
            ],
        ),
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
        migrations.CreateModel(
            name='GenWEC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Powerplant',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('capacity', models.FloatField(blank=True, null=True)),
                ('chp', models.TextField(blank=True, null=True)),
                ('com_month', models.FloatField(blank=True, null=True)),
                ('com_year', models.FloatField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('decom_month', models.BigIntegerField(blank=True, null=True)),
                ('decom_year', models.BigIntegerField(blank=True, null=True)),
                ('efficiency', models.FloatField(blank=True, null=True)),
                ('energy_source_level_1', models.TextField(blank=True, null=True)),
                ('energy_source_level_2', models.TextField(blank=True, null=True)),
                ('energy_source_level_3', models.TextField(blank=True, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('state', models.TextField(blank=True, null=True)),
                ('technology', models.TextField(blank=True, null=True)),
                ('thermal_capacity', models.FloatField(blank=True, null=True)),
                ('coastdat2', models.FloatField(blank=True, null=True)),
                ('capacity_in', models.FloatField(blank=True, null=True)),
                ('federal_state', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegBioReserve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegBirdProtArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
                ('gebietsnam', models.CharField(max_length=254, null=True)),
                ('gebietsnum', models.CharField(max_length=254, null=True)),
                ('rechtsgrun', models.CharField(max_length=254, null=True)),
                ('erfassungs', models.CharField(max_length=254, null=True)),
                ('info_konta', models.CharField(max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegBirdProtAreaB200',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegDeadZoneHard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegDeadZoneSoft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegFFHProtArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
                ('gebietsnam', models.CharField(max_length=254, null=True)),
                ('gebietsnum', models.CharField(max_length=254, null=True)),
                ('rechtsgrun', models.CharField(max_length=254, null=True)),
                ('erfassungs', models.CharField(max_length=254, null=True)),
                ('info_konta', models.CharField(max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegFFHProtAreaB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegForest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegInfrasAviation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegInfrasHvgrid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegInfrasRailway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegInfrasRoad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegLandscProtArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegLandscProtAreaParts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
                ('gebietsnam', models.CharField(max_length=254, null=True)),
                ('gebietsnum', models.CharField(max_length=254, null=True)),
                ('rechtsgrun', models.CharField(max_length=254, null=True)),
                ('erfassungs', models.CharField(max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegMun',
            fields=[
                ('ags', models.IntegerField(primary_key=True, serialize=False)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=3035)),
                ('gen', models.CharField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegNatureMonum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegNaturePark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegNatureProtArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
                ('gebietsnam', models.CharField(max_length=254, null=True)),
                ('gebietsnum', models.CharField(max_length=254, null=True)),
                ('rechtsgrun', models.CharField(max_length=254, null=True)),
                ('schutzzone', models.CharField(max_length=254, null=True)),
                ('erfassungs', models.CharField(max_length=254, null=True)),
                ('info_konta', models.CharField(max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegPrioAreaAgri',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegPrioAreaCult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
                ('bezeich_2', models.CharField(max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegPrioAreaFloodProt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
                ('bemerkunge', models.CharField(max_length=254, null=True)),
                ('bezeich_2', models.CharField(max_length=254, null=True)),
                ('bezeich_3', models.CharField(max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegPrioAreaNature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegPrioAreaRes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
                ('bezeich_2', models.CharField(max_length=254, null=True)),
                ('bezeich_3', models.CharField(max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegPrioAreaWater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegPrioAreaWEC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
                ('bezeich_2', models.CharField(max_length=254, null=True)),
                ('bezeich_3', models.CharField(max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegResidArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegResidAreaB1000',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegResidAreaB500',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegRetentAreaAgri',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegRetentAreaEcosys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegWaterProtArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=3035)),
                ('gebietsnam', models.CharField(max_length=254, null=True)),
                ('gebietsnum', models.CharField(max_length=254, null=True)),
                ('rechtsgrun', models.CharField(max_length=254, null=True)),
                ('schutzzone', models.CharField(max_length=254, null=True)),
                ('erfassungs', models.CharField(max_length=254, null=True)),
                ('amtsblatt', models.CharField(max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RpAbwBound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(null=True, srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MunData',
            fields=[
                ('ags', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='stemp_abw.RegMun')),
                ('area', models.FloatField(null=True)),
                ('pop_2011', models.IntegerField(null=True)),
                ('pop_2017', models.IntegerField(null=True)),
                ('pop_2030', models.IntegerField(null=True)),
                ('pop_2050', models.IntegerField(null=True)),
                ('total_living_space', models.FloatField(null=True)),
                ('gen_count_wind', models.FloatField(null=True)),
                ('gen_count_pv_roof_small', models.FloatField(null=True)),
                ('gen_count_pv_roof_large', models.FloatField(null=True)),
                ('gen_count_pv_ground', models.FloatField(null=True)),
                ('gen_count_hydro', models.FloatField(null=True)),
                ('gen_count_bio', models.FloatField(null=True)),
                ('gen_count_steam_turbine', models.FloatField(null=True)),
                ('gen_count_combined_cycle', models.FloatField(null=True)),
                ('gen_count_sewage_landfill_gas', models.FloatField(null=True)),
                ('gen_count_storage', models.FloatField(null=True)),
                ('gen_capacity_wind', models.FloatField(null=True)),
                ('gen_capacity_pv_roof_small', models.FloatField(null=True)),
                ('gen_capacity_pv_roof_large', models.FloatField(null=True)),
                ('gen_capacity_pv_ground', models.FloatField(null=True)),
                ('gen_capacity_hydro', models.FloatField(null=True)),
                ('gen_capacity_bio', models.FloatField(null=True)),
                ('gen_capacity_steam_turbine', models.FloatField(null=True)),
                ('gen_capacity_combined_cycle', models.FloatField(null=True)),
                ('gen_capacity_sewage_landfill_gas', models.FloatField(null=True)),
                ('gen_capacity_storage', models.FloatField(null=True)),
                ('gen_el_energy_wind', models.FloatField(null=True)),
                ('gen_el_energy_pv_roof', models.FloatField(null=True)),
                ('gen_el_energy_pv_ground', models.FloatField(null=True)),
                ('gen_el_energy_hydro', models.FloatField(null=True)),
                ('dem_el_peak_load_hh', models.FloatField(null=True)),
                ('dem_el_peak_load_rca', models.FloatField(null=True)),
                ('dem_el_peak_load_ind', models.FloatField(null=True)),
                ('dem_el_energy_hh', models.FloatField(null=True)),
                ('dem_el_energy_rca', models.FloatField(null=True)),
                ('dem_el_energy_ind', models.FloatField(null=True)),
                ('dem_th_peak_load_hh', models.FloatField(null=True)),
                ('dem_th_peak_load_rca', models.FloatField(null=True)),
                ('dem_th_peak_load_ind', models.FloatField(null=True)),
                ('dem_th_energy_hh', models.FloatField(null=True)),
                ('dem_th_energy_hh_efh', models.FloatField(null=True)),
                ('dem_th_energy_hh_mfh', models.FloatField(null=True)),
                ('dem_th_energy_hh_efh_spec', models.FloatField(null=True)),
                ('dem_th_energy_hh_mfh_spec', models.FloatField(null=True)),
                ('dem_th_energy_rca', models.FloatField(null=True)),
                ('dem_th_energy_ind', models.FloatField(null=True)),
                ('dem_th_energy_hh_per_capita', models.FloatField(null=True)),
                ('dem_th_energy_total_per_capita', models.FloatField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='powerplant',
            name='ags',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='stemp_abw.RegMun'),
        ),
        migrations.AddField(
            model_name='feedints',
            name='ags',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='stemp_abw.RegMun'),
        ),
        migrations.AddField(
            model_name='demandts',
            name='ags',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='stemp_abw.RegMun'),
        ),
        migrations.CreateModel(
            name='RegMunStats',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('stemp_abw.regmun',),
        ),
    ]
