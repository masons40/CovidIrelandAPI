from django.db import models

class CovidStats(models.Model):
    date = models.DateField(auto_now=False, unique=True)
    deaths_today = models.IntegerField()
    diagnosed_today = models.IntegerField()
    hospitalised = models.IntegerField()
    total_diagnosed = models.IntegerField()
    total_death = models.IntegerField()
    healthcare_workers_diagnosed = models.IntegerField()
    total_clusters = models.IntegerField()
    cluster_diagnosed = models.IntegerField()
    icu = models.IntegerField()
    median_age = models.IntegerField()

    def __str__(self):
        return 'CovidStats_history_' + str(self.date)

    class Meta:
        verbose_name_plural = "Covid Data"
        verbose_name = "Covid Data"
        unique_together = ("date", "deaths_today", "diagnosed_today", "hospitalised", "total_diagnosed", "total_death",
                           "healthcare_workers_diagnosed", "total_clusters", "cluster_diagnosed", "icu", "median_age")


class CountyStat(models.Model):
    date = models.DateField(auto_now=False)
    county_name = models.CharField(max_length=150)
    number_of_cases = models.IntegerField()
    percentage_of_cases = models.DecimalField(decimal_places=2, max_digits=4)
    # change_since_yesterday = models.IntegerField()

    def __str__(self):
        return self.county_name + '_history_' + str(self.date)

    class Meta:
        verbose_name_plural = "County"
        verbose_name = "County"


class GenderStats(models.Model):
    date = models.DateField(auto_now=False)
    male = models.IntegerField()
    female = models.IntegerField()
    other = models.IntegerField()

    def __str__(self):
        return 'Gender_history_' + str(self.date)

    class Meta:
        verbose_name_plural = "Gender Data"
        verbose_name = "Gender Data"


class TransmissionStats(models.Model):
    date = models.DateField(auto_now=False)
    community_transmission = models.DecimalField(decimal_places=2, max_digits=4)
    close_contact = models.DecimalField(decimal_places=2, max_digits=4)
    travel_abroad = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return 'Transmission_history_' + str(self.date)

    class Meta:
        verbose_name_plural = "Transmission Data"
        verbose_name = "Transmission Data"


class HospitalBarChartStats(models.Model):
    date = models.DateField(auto_now=False)
    _0_4 = models.IntegerField()
    _5_14 = models.IntegerField()
    _15_24 = models.IntegerField()
    _25_34 = models.IntegerField()
    _35_44 = models.IntegerField()
    _45_54 = models.IntegerField()
    _55_64 = models.IntegerField()
    _65_74 = models.IntegerField()
    _75_84 = models.IntegerField()
    _85_over = models.IntegerField()
    unknown_age = models.IntegerField()

    def __str__(self):
        return 'Hospital_history_' + str(self.date)

    class Meta:
        verbose_name_plural = "Hospital Data"
        verbose_name = "Hospital Data"


class AgeBarChartStats(models.Model):
    date = models.DateField(auto_now=False)
    _0_4 = models.IntegerField()
    _5_14 = models.IntegerField()
    _15_24 = models.IntegerField()
    _25_34 = models.IntegerField()
    _35_44 = models.IntegerField()
    _45_54 = models.IntegerField()
    _55_64 = models.IntegerField()
    _65_74 = models.IntegerField()
    _75_84 = models.IntegerField()
    _85_over = models.IntegerField()
    unknown_age = models.IntegerField()

    def __str__(self):
        return 'Age_history_' + str(self.date)

    class Meta:
        verbose_name_plural = "Age Data"
        verbose_name = "Age Data"


class CovidHistory(models.Model):
    date = models.DateField(auto_now=False)
    covid_stats = models.OneToOneField(
        CovidStats,
        on_delete=models.CASCADE,
        blank=True
    )

    hospital_data = models.OneToOneField(
        HospitalBarChartStats,
        on_delete=models.CASCADE,
        blank=True
    )

    age_data = models.OneToOneField(
        AgeBarChartStats,
        on_delete=models.CASCADE,
        blank=True
    )

    transmission_data = models.OneToOneField(
        TransmissionStats,
        on_delete=models.CASCADE,
        blank=True
    )

    gender_data = models.OneToOneField(
        GenderStats,
        on_delete=models.CASCADE,
        blank=True
    )

    county_data = models.ManyToManyField(
        CountyStat
    )

    def __str__(self):
        return 'Covid_history_' + str(self.date)

    class Meta:
        verbose_name_plural = "Covid History"
        verbose_name = "Covid History"