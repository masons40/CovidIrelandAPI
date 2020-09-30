from datetime import date
from covidtracker.models import CovidStats, HospitalBarChartStats, AgeBarChartStats, TransmissionStats, GenderStats, \
    CountyStat, CovidHistory
import requests
from bs4 import BeautifulSoup


def create_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    information_date = find_date_datalink(soup)
    death_diagnosed_data = soup.find_all('div', {'class': 'row'})
    table_data = soup.find_all('table')
    p_tag_data = death_diagnosed_data[5].find_all('p')
    death_data = p_tag_data[0]
    diagnosed_data = p_tag_data[2:5]

    # print(soup.prettify())
    deaths = get_deaths(death_data.text)
    diagnosed = get_diagnosed(diagnosed_data)

    # hospital stats
    hospital_data_list = []
    for td in table_data[0].find_all('tr'):
        td_data = td.find_all('td')
        hospital_data_list.append(td_data[1].text)

    CovidStats(
        date=information_date,
        deaths_today=deaths,
        diagnosed_today=diagnosed,
        total_diagnosed=int(hospital_data_list[0].replace(',', '')),
        hospitalised=int(hospital_data_list[1].replace(',', '')),
        total_death=int(hospital_data_list[3].replace(',', '')),
        healthcare_workers_diagnosed=int(hospital_data_list[4].replace(',', '')),
        total_clusters=int(hospital_data_list[5].replace(',', '')),
        cluster_diagnosed=int(hospital_data_list[6].replace(',', '')),
        icu=int(hospital_data_list[2].replace(',', '')),
        median_age=int(hospital_data_list[7].replace(',', ''))
    ).save()

    covid_stats = CovidStats.objects.get(date=information_date)

    # gender_data
    gender = table_data[1].find_all('tr')
    GenderStats(
        date=information_date,
        female=float(gender[1].find_all()[1].text.replace(',', '')),
        male=float(gender[2].find_all()[1].text.replace(',', '')),
        other=float(gender[3].find_all()[1].text.replace(',', '')),
    ).save()

    transmission_data = table_data[3].find_all('tr')
    transmission_data = clean_transmission_data(transmission_data)

    TransmissionStats(
        date=information_date,
        community_transmission=transmission_data['community transmission'],
        close_contact=transmission_data['close contact with confirmed case'],
        travel_abroad=transmission_data['travel abroad'],
    ).save()

    hospital_data = table_data[4].find_all('tr')[1:]
    # hospital_data = filter_for_data(hospital_data)

    HospitalBarChartStats(
        date=information_date,
        _0_4=int(hospital_data[0].find_all('td')[1].text.replace(',', '')),
        _5_14=int(hospital_data[1].find_all('td')[1].text.replace(',', '')),
        _15_24=int(hospital_data[2].find_all('td')[1].text.replace(',', '')),
        _25_34=int(hospital_data[3].find_all('td')[1].text.replace(',', '')),
        _35_44=int(hospital_data[4].find_all('td')[1].text.replace(',', '')),
        _45_54=int(hospital_data[5].find_all('td')[1].text.replace(',', '')),
        _55_64=int(hospital_data[6].find_all('td')[1].text.replace(',', '')),
        _65_74=int(hospital_data[7].find_all('td')[1].text.replace(',', '')),
        _75_84=int(hospital_data[8].find_all('td')[1].text.replace(',', '')),
        _85_over=int(hospital_data[9].find_all('td')[1].text.replace(',', '')),
        unknown_age=int(hospital_data[10].find_all('td')[1].text.replace(',', '')),
    ).save()

    age_data = table_data[2].find_all('tr')[1:]

    AgeBarChartStats(
        date=information_date,
        _0_4=int(age_data[0].find_all('td')[1].text.replace(',', '')),
        _5_14=int(age_data[1].find_all('td')[1].text.replace(',', '')),
        _15_24=int(age_data[2].find_all('td')[1].text.replace(',', '')),
        _25_34=int(age_data[3].find_all('td')[1].text.replace(',', '')),
        _35_44=int(age_data[4].find_all('td')[1].text.replace(',', '')),
        _45_54=int(age_data[5].find_all('td')[1].text.replace(',', '')),
        _55_64=int(age_data[6].find_all('td')[1].text.replace(',', '')),
        _65_74=int(age_data[7].find_all('td')[1].text.replace(',', '')),
        _75_84=int(age_data[8].find_all('td')[1].text.replace(',', '')),
        _85_over=int(age_data[9].find_all('td')[1].text.replace(',', '')),
        unknown_age=int(age_data[10].find_all('td')[1].text.replace(',', '')),
    ).save()

    # County data

    counties = {}
    county_data_list = table_data[5].find_all('tr')[1:]
    for county in county_data_list:
        county_list = county.find_all('td')
        counties[county_list[0].text] = {'cases': county_list[1].text.replace(',', ''),
                                         'percentage': float(county_list[2].text.replace("%", ""))}

    for key in counties:
        CountyStat(
            date=information_date,
            county_name=key,
            number_of_cases=counties[key]['cases'],
            percentage_of_cases=counties[key]['percentage'],
        ).save()

    CovidHistory(
        date=information_date,
        covid_stats=covid_stats,
        hospital_data=HospitalBarChartStats.objects.get(date=information_date),
        age_data=AgeBarChartStats.objects.get(date=information_date),
        transmission_data=TransmissionStats.objects.get(date=information_date),
        gender_data=GenderStats.objects.get(date=information_date)
    ).save()
    ch = CovidHistory.objects.get(date=information_date)
    ch.county_data.set(CountyStat.objects.all().filter(date=information_date))

    return {'data': CovidHistory.objects.get(date=information_date)}

def find_date(paragraph_text):
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
              'november', 'december']
    paragraph_text_stripped = paragraph_text.split(';')[0].strip().split(' ')
    found_month = months.index(paragraph_text_stripped[1].lower())
    date_found = date(int(paragraph_text_stripped[2]), int(found_month) + 1, int(paragraph_text_stripped[0]))
    return date_found

def find_latest_date():
    URL = 'https://www.gov.ie/en/publications/?type=press_releases&organisation=department-of-health&page=1'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    news_url = soup.find_all('div', {"role": "region"})[2].find_all('li')

    li_index = 0
    counter = 0
    match_sentence = 'statement-from-the-national-public'
    while counter < len(news_url):
        if match_sentence in news_url[li_index].find('a')['href']:
            li_index = counter
            counter = len(news_url)
        counter += 1

    paragraph_text = news_url[li_index].find('p').text
    return find_date(paragraph_text), news_url[li_index].find('a')['href']


def find_date_datalink(soup):
    date_found = soup.find_all('time')[0]['datetime']
    return date.fromisoformat(date_found)



def clean_transmission_data(transmission_data):
    check_words = ['community transmission', 'close contact with confirmed case', 'travel abroad']
    cleaned_data = {}
    for tr in transmission_data:
        td_data = tr.find_all('td')
        if td_data[0].text.lower() in check_words:
            cleaned_data[td_data[0].text.lower()] = float(td_data[1].text.replace('%', ''))

    return cleaned_data

def get_deaths(text):
    word_numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                    "twelve", "thirteen", "fourteen", "fifteen",
                    "sixteen", "seventeen", "eighteen", "nineteen"]
    text_list = text.split()
    if 'no' in text_list and ('deaths' in text_list or 'death' in text_list):
        return 0
    else:
        for word in text_list:
            check_word = word.replace(',', '').replace('*', '').lower()
            if check_word.isnumeric():
                return int(word.replace(',', '').replace('*', ''))
            elif check_word in word_numbers:
                return word_numbers.index(check_word)

        return 0


def get_diagnosed(text_pragraphs):
    for p_tag in text_pragraphs:
        text_list = p_tag.text.split()
        if p_tag.text:
            if 'no' in text_list and ('diagnosed' in text_list):
                print(text_list)
                return 0
            elif 'confirmed' in text_list:
                print(text_list)
                try:
                    return int(text_list[text_list.index('confirmed') - 1].replace('*', ''))
                except ValueError:
                    return int(text_list[text_list.index('confirmed') - 2].replace('*', ''))
    return 0


def find_urls():
    url_list = {}
    URL = 'https://www.gov.ie/en/publications/?type=press_releases&organisation=department-of-health&page='
    end_date = date.fromisoformat('2020-05-09')
    page_start = 1
    match_sentence = 'statement-from-the-national-public'
    while True:
        page = requests.get(URL + str(page_start))
        soup = BeautifulSoup(page.content, 'html.parser')
        news_url = soup.find_all('div', {"role": "region"})[2].find_all('li')
        for i in news_url:
            anchor_href = i.find('a')['href']
            if match_sentence in anchor_href:
                data_date = find_date(i.find('p').text)

                url_list[data_date] = ('https://www.gov.ie/' + anchor_href)
                if data_date == end_date:
                    return url_list
        page_start += 1