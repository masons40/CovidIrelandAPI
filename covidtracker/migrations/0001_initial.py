# Generated by Django 3.0.7 on 2020-08-01 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgeBarChartStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_0_4', models.IntegerField()),
                ('_5_14', models.IntegerField()),
                ('_15_24', models.IntegerField()),
                ('_25_34', models.IntegerField()),
                ('_35_44', models.IntegerField()),
                ('_45_54', models.IntegerField()),
                ('_55_64', models.IntegerField()),
                ('_65_74', models.IntegerField()),
                ('_75_84', models.IntegerField()),
                ('_85_over', models.IntegerField()),
                ('unknown_age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CountyStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('county_name', models.CharField(max_length=150)),
                ('number_of_cases', models.IntegerField()),
                ('percentage_of_cases', models.DecimalField(decimal_places=3, max_digits=3)),
                ('change_since_yesterday', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CovidStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deaths_today', models.IntegerField()),
                ('diagnosed_today', models.IntegerField()),
                ('total_diagnosed', models.IntegerField()),
                ('total_death', models.IntegerField()),
                ('healthcare_workers_diagnosed', models.IntegerField()),
                ('total_clusters', models.IntegerField()),
                ('cluster_diagnosed', models.IntegerField()),
                ('icu', models.IntegerField()),
                ('median_age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DailyData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('deaths', models.IntegerField()),
                ('diagnosed', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GenderStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('male', models.IntegerField()),
                ('female', models.IntegerField()),
                ('other', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HospitalBarChartStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_0_4', models.IntegerField()),
                ('_5_14', models.IntegerField()),
                ('_15_24', models.IntegerField()),
                ('_25_34', models.IntegerField()),
                ('_35_44', models.IntegerField()),
                ('_45_54', models.IntegerField()),
                ('_55_64', models.IntegerField()),
                ('_65_74', models.IntegerField()),
                ('_75_84', models.IntegerField()),
                ('_85_over', models.IntegerField()),
                ('unknown_age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TransmissonStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community_transmission', models.DecimalField(decimal_places=3, max_digits=3)),
                ('close_contact', models.DecimalField(decimal_places=3, max_digits=3)),
                ('travel_abroad', models.DecimalField(decimal_places=3, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='CovidHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='covidtracker.AgeBarChartStats')),
                ('county_data', models.ManyToManyField(to='covidtracker.CountyStat')),
                ('covid_stats', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='covidtracker.CovidStats')),
                ('gender_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='covidtracker.GenderStats')),
                ('hospital_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='covidtracker.HospitalBarChartStats')),
                ('transmission_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='covidtracker.TransmissonStats')),
            ],
        ),
    ]
