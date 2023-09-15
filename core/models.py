from django.db import models

# Create your models here.
class Exchanges(models.Model):
    exchange_name = models.CharField(max_length=250)
    exchange_id = models.CharField(max_length=250)

    
class TimePeriods(models.Model):
    period_name = models.CharField(max_length=250)
    period_id = models.CharField(max_length=250)


class Assets(models.Model):
    asset_name = models.CharField(max_length=250)
    asset_id = models.CharField(max_length=250)
    is_crypto = models.IntegerField()