# Generated by Django 3.0.7 on 2020-08-02 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covidtracker', '0005_auto_20200801_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='covidstats',
            name='hospitalised',
            field=models.IntegerField(default=1211),
            preserve_default=False,
        ),
    ]
