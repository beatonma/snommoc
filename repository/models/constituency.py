from django.db import models


class Constituency(models.Model):
    name = models.CharField(max_length=64)
    mp = models.OneToOneField('Mp', on_delete=models.CASCADE, null=True)

    ordinance_survey_name = models.CharField(max_length=64, null=True)
    gss_code = models.CharField(
        max_length=12, null=True,
        help_text='Government Statistical Service ID')
    constituency_type = models.CharField(
        max_length=10, null=True,
        help_text='Borough, county...')


class ConstituencyBoundary(models.Model):
    constituency = models.OneToOneField(Constituency, on_delete=models.CASCADE)
    boundary = models.TextField(help_text='KML file content')
