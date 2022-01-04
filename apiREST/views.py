from django.shortcuts import render
from rest_framework import viewsets
from .models import Property
from .models import Activity
from .models import Survey

from .serializers import PropertySerializers
from .serializers import ActivitySerializers
from .serializers import SurveySerializers

# Create your views here.
class PropertyViewsets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post','put','delete']
    queryset = Property.objects.all()
    serializer_class = PropertySerializers

class ActivityViewsets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post','put','delete']
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializers

class SurveyViewsets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post','put','delete']
    queryset = Survey.objects.all()
    serializer_class = SurveySerializers