# Generated by Django 2.1.1 on 2018-10-09 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stemp_abw', '0027_regbirdprotarea'),
    ]

    operations = [
        migrations.RenameField(
            model_name='regbirdprotarea',
            old_name='amtsblatt',
            new_name='info_konta',
        ),
        migrations.RemoveField(
            model_name='regbirdprotarea',
            name='schutzzone',
        ),
    ]