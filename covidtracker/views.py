from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, User
from django.shortcuts import render
from .dataFunctions.DataCreator import find_urls, create_data
from .models import CovidStats, HospitalBarChartStats, AgeBarChartStats, TransmissionStats, GenderStats, \
    CountyStat, CovidHistory
from datetime import date, timedelta
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from .serializers import CovidStatsSerializer, CountyStatSerializer, CovidHistorySerializer, AgeBarChartStatsSerializer, \
    HospitalBarChartStatsSerializer, GenderStatsSerializer, TransmissionStatsSerializer


# Create your views here.
def home(request):
    userReg = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return render(request, 'covidtracker/signup.html', {'name': username, 'userLog': True})
        else:
            return render(request, 'covidtracker/signup.html', {'errors': form.error_messages, 'form': userReg, 'userLog': False})

    return render(request, 'covidtracker/signup.html', {'form': userReg, 'userLog': False})


def logout_view(request):
    userReg = UserCreationForm()
    logout(request)
    return render(request, 'covidtracker/signup.html', {'form': userReg, 'userLog': False})


def loginuser(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    userReg = UserCreationForm()
    if user is not None:
        login(request, user)
        return render(request, 'covidtracker/signup.html', {'name': username, 'userLog': True})
    else:
        print("error")

    return render(request, 'covidtracker/signup.html', {'userLog': False, 'form': userReg, 'errors': user})


def slform(request):
    info = {}
    if request.user is not None:
        info['userLog'] = True
        info['name'] = request.user.username
    else:
        info['userLog'] = False
    info['form'] = UserCreationForm()
    return render(request, 'covidtracker/signup.html', info)


def about(request):
    userReg = UserCreationForm()
    info = {}
    if request.user is not None:
        info['userLog'] = True
        info['name'] = request.user.username
    else:
        info['userLog'] = False
    return render(request, 'covidtracker/about.html', info)


def endpoints(request):
    info = {}
    if request.user is not None:
        info['userLog'] = True
        info['name'] = request.user.username
    else:
        info['userLog'] = False
    return render(request, 'covidtracker/endpoints.html', info)


def index(request):
    current_date = date.today()
    yesterday = current_date - timedelta(days=3)
    if request.method == 'POST':
        input_date = request.POST['date']
        context = {'data': CovidHistory.objects.get(date=date.fromisoformat(input_date)),
                   'date': date.fromisoformat(input_date)}
    # else:
    #     latest_url_date, latest_url = find_latest_date()
    #     if latest_url_date == current_date:
    #         try:
    #             context = {'data': CovidHistory.objects.get(date=latest_url_date),
    #                        'date': latest_url_date}
    #         except ObjectDoesNotExist:
    #             context = create_data('https://www.gov.ie' + latest_url)
    #             context['date'] = latest_url_date
    #     else:
    #         context = {'data': CovidHistory.objects.get(date=yesterday),
    #                    'date': yesterday}

    return render(request, 'covidtracker/index.html',
                  {'data': CovidHistory.objects.get(date=yesterday), 'date': yesterday})


@login_required
def upload_all(request):
    yesterday = date.today() - timedelta(days=1)
    bad_dates = [date.fromisoformat('2020-07-16'), date.fromisoformat('2020-07-05'), date.fromisoformat('2020-07-04'),
                 date.fromisoformat('2020-07-02'), date.fromisoformat('2020-06-28'), date.fromisoformat('2020-06-27'),
                 date.fromisoformat('2020-05-20')]
    data_urls = find_urls()
    for key, url in data_urls.items():
        if key not in bad_dates:
            print("creating data for:", url, "(", key, ")")
            create_data(url)
            print("data created\n\n")
    print("finished upload")

    context = {'data': CovidHistory.objects.get(date=yesterday), 'date': yesterday}
    return render(request, 'covidtracker/index.html', context)


@login_required
def data_upload(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['url_link']
        context = create_data(url)
        input_date = request.POST['date']

    return render(request, 'covidtracker/dataupload.html', context)


@login_required
def delete_data(request):
    CovidHistory.objects.all().delete()
    HospitalBarChartStats.objects.all().delete()
    CountyStat.objects.all().delete()
    CovidStats.objects.all().delete()
    AgeBarChartStats.objects.all().delete()
    GenderStats.objects.all().delete()
    TransmissionStats.objects.all().delete()

    return render(request, 'covidtracker/dataupload.html', {})


class CovidStatsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = CovidStats.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = CovidStatsSerializer
    permission_classes = [permissions.IsAuthenticated]


class CountyStatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = CountyStat.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = CountyStatSerializer
    permission_classes = [permissions.IsAuthenticated]


class CovidHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = CovidHistory.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = CovidHistorySerializer
    permission_classes = [permissions.IsAuthenticated]


class AgeBarChartStatsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = AgeBarChartStats.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = AgeBarChartStatsSerializer
    permission_classes = [permissions.IsAuthenticated]


class HospitalBarChartStatsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = HospitalBarChartStats.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = HospitalBarChartStatsSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransmissionStatsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = TransmissionStats.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = TransmissionStatsSerializer
    permission_classes = [permissions.IsAuthenticated]


class GenderStatsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = GenderStats.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = GenderStatsSerializer
    permission_classes = [permissions.IsAuthenticated]
