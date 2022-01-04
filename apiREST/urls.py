from rest_framework import routers
from django.urls import path, include
from .views import PropertyViewsets
from .views import ActivityViewsets
from .views import SurveyViewsets

router = routers.DefaultRouter()
router.register('property',PropertyViewsets)
router.register('activity',ActivityViewsets)
router.register('survey',SurveyViewsets)

urlpatterns = [
    path('api/', include(router.urls)),
]