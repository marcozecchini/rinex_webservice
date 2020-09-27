from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from enum import Enum
from django.utils.translation import ugettext_lazy as _

license_list = (
    ("CC_BY_IGO" , "CC BY-IGO"),
    ("CC_BY" , "CC BY"),
    ("CC_BY_SA", "CC BY-SA"),
    ("CC0", "CC0"), 
    ("ODC_ODbL" , "ODC-ODbL"),
    ("ODC_BY" , "ODC-BY"),
    ("PDDL" , "PDDL"),
)

class SystemInfo(models.Field):
    def __init__(self, SYS, number, dual):
        self.SYS = SYS
        self.number = number
        self.dual = dual

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    def __str__(self):
        return self.username

class RinexMetadata(models.Model):
    min_lon = models.FloatField()
    min_lat = models.FloatField()
    max_lon = models.FloatField()
    max_lat = models.FloatField()

    receiver_info = models.CharField(max_length=100)
    antenna_info = models.CharField(max_length=100)

    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()

    system_info = ArrayField(models.CharField(max_length=10))
    number_sys_info = ArrayField(models.IntegerField())
    dual_frequency = ArrayField(models.BooleanField())
    
    file_rinex = models.CharField(max_length=150)
    upload_datetime = models.DateTimeField(auto_now_add=True) 

    licence = models.CharField(max_length=300, default=license_list[3][0])

    def __str__(self):
        return str(self.start_time)+"-"+str(self.finish_time)
