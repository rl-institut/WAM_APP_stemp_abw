# Generated by Django 2.1.3 on 2019-02-13 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0053_delete_osmpowergen'),
    ]

    operations = [
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
                ('ags', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='stemp_abw.RegMun')),
            ],
        ),
    ]
