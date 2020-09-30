from django import template
from ..models import CovidStats, CountyStat
import datetime

register = template.Library()


@register.filter(name='county_list')
def county_list(data):
    print(data)
    print(type(data))
    county_data = [['Location', 'Parent', 'Number of Cases', 'empty', '% of total'],
                   ['Ireland', '', 0, 0, 0]]
    for key in data:
        county_data.append(
            [key.county_name, 'Ireland', key.number_of_cases, float(key.number_of_cases * key.percentage_of_cases),
             float(key.percentage_of_cases)])
    return county_data


@register.filter(name='barchart_data')
def barchart_data(data):
    return [data._0_4, data._5_14, data._15_24, data._25_34, data._35_44, data._45_54, data._55_64, data._65_74,
            data._75_84,
            data._85_over,
            data.unknown_age]


@register.filter(name='trend_data')
def line_data(data):
    labels = []
    deaths = []
    diagnosed = []
    trends_data = CovidStats.objects.order_by('date')
    for trend_data in trends_data:
        labels.append(str(trend_data.date))
        deaths.append(trend_data.deaths_today)
        diagnosed.append(trend_data.diagnosed_today)

    data_dictionary = {'deaths': deaths, 'diagnosed': diagnosed, 'labels': labels}
    return data_dictionary


@register.filter(name='county_data_all')
def county_data_all(data):
    counties_data = CountyStat.objects.order_by('date').reverse()
    dates = [c.date for c in counties_data]
    dates = list(dict.fromkeys(dates))
    print(dates)
    latest_date = counties_data[0].date
    return {}
