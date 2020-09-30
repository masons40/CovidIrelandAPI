from rest_framework import serializers
from .models import CovidStats, CountyStat, CovidHistory, HospitalBarChartStats, AgeBarChartStats, GenderStats, \
    TransmissionStats


class CovidStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CovidStats
        fields = ['id', 'date', 'deaths_today', 'diagnosed_today', 'hospitalised', 'total_diagnosed', 'total_death',
                  'healthcare_workers_diagnosed',
                  'total_clusters', 'cluster_diagnosed', 'icu', 'median_age']


class CountyStatSerializer(serializers.ModelSerializer):

    class Meta:
        model = CountyStat
        fields = ['id', 'date', 'county_name', 'number_of_cases', 'percentage_of_cases']


class CovidHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CovidHistory
        fields = ['id', 'date', 'covid_stats', 'hospital_data', 'age_data', 'transmission_data', 'gender_data', 'county_data']


class AgeBarChartStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeBarChartStats
        fields = ['id', 'date', '_0_4', '_5_14', '_15_24', '_25_34', '_35_44', '_45_54', '_55_64', '_65_74', '_75_84', '_85_over', 'unknown_age']


class HospitalBarChartStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalBarChartStats
        fields = ['id', 'date', '_0_4', '_5_14', '_15_24', '_25_34', '_35_44', '_45_54', '_55_64', '_65_74', '_75_84', '_85_over', 'unknown_age']


class TransmissionStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmissionStats
        fields = ['id', 'date', 'community_transmission', 'close_contact', 'travel_abroad']


class GenderStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenderStats
        fields = ['id', 'date', 'male', 'female', 'other']