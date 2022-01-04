from django.db.models import fields
from rest_framework import serializers
from .models import Property
from .models import Activity
from .models import Survey

class PropertySerializers(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class ActivitySerializers(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class SurveySerializers(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'