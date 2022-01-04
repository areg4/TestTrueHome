from django.db import models
from django.db.models import JSONField

# Create your models here.
class Property(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    address = models.TextField(max_length=500,null=False,blank=False)
    description = models.TextField(max_length=500,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True,null=False,blank=False)
    updated_at =models.DateTimeField(auto_now=True,null=False,blank=False)
    disabled_at = models.DateTimeField()
    status = models.CharField(max_length=35,null=False,blank=False)

class Activity(models.Model):
    property_id = models.ForeignKey(Property, null=False,blank=False, on_delete=models.CASCADE)
    schedule = models.DateTimeField(null=False,blank=False)
    title = models.CharField(max_length=255, null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True,null=False,blank=False)
    updated_at = models.DateTimeField(auto_now=True,null=False,blank=False)
    status = models.CharField(max_length=35, null=False,blank=False)

class Survey(models.Model):
    activity_id = models.ForeignKey(Activity,null=False,blank=False,on_delete=models.CASCADE)
    answers = JSONField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False,blank=False)

