from django.contrib import admin
from .models import CovidStats, CountyStat, CovidHistory, HospitalBarChartStats, AgeBarChartStats, GenderStats, TransmissionStats

# Register your models here.

admin.site.register(CovidStats)
admin.site.register(CountyStat)
admin.site.register(CovidHistory)
admin.site.register(HospitalBarChartStats)
admin.site.register(AgeBarChartStats)
admin.site.register(GenderStats)
admin.site.register(TransmissionStats)