# Generated by Django 2.1.3 on 2019-03-13 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0007_auto_20190313_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='data',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='stemp_abw.ScenarioData'),
            preserve_default=False,
        ),
    ]
