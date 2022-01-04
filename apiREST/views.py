from datetime import datetime, timedelta
from django.utils.timezone import now
from django.shortcuts import render
from rest_framework import viewsets
from django.core.exceptions import ValidationError
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from .models import Property
from .models import Activity
from .models import Survey
from .models import StatusEnum

from .serializers import PropertySerializers
from .serializers import ActivitySerializers
from .serializers import SurveySerializers

# Create your views here.
class PropertyViewsets(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Property.objects.all()
    serializer_class = PropertySerializers

class ActivityViewsets(viewsets.ModelViewSet):
    http_method_names = ['get', 'post','put','delete']
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializers

    def create(self, request, *args, **kwargs):
        try:
            property = Property.objects.get(id=request.data['property_id'])        
            if StatusEnum(property.status) is not StatusEnum.ACTIVE:
                dataR = {
                    "msg" : "Propiedad DESACTIVADA"
                }
                return Response(data=dataR,status=HTTP_400_BAD_REQUEST)
            
            activities = Activity.objects.filter(
                        schedule__range=(datetime.strptime(request.data['schedule'],"%Y-%m-%d %H:%M:%S") - timedelta(hours=1),
                        datetime.strptime(request.data['schedule'],"%Y-%m-%d %H:%M:%S") + timedelta(hours=1)),
                        property_id=request.data['property_id'])
            if len(activities)>0:
                dataR = {
                    "msg" : "Actividades programadas para esta propiedad en este rango de fecha y hora"
                }
                return Response(data=dataR,status=HTTP_400_BAD_REQUEST)
            return super().create(request, *args, **kwargs)
        except Exception as e:
            dataEx = {
                "msg" : e
            }
            return Response(data=dataEx,status=HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        activity = Activity.objects.get(pk=pk)
        try:
            activities = Activity.objects.filter(
                        schedule__range=(datetime.strptime(request.data['schedule'],"%Y-%m-%d %H:%M:%S") - timedelta(hours=1),
                        datetime.strptime(request.data['schedule'],"%Y-%m-%d %H:%M:%S") + timedelta(hours=1)),
                        property_id=activity.property_id.id)
            if len(activities)>0:
                dataR = {
                    "msg" : "Actividades programadas para esta propiedad en este rango de fecha y hora"
                }
                return Response(data=dataR,status=HTTP_400_BAD_REQUEST)

            if StatusEnum(activity.status) is not StatusEnum.ACTIVE:
                dataR = {
                    "msg" : "Actividad DESACTIVADA"
                }
                return Response(data=dataR,status=HTTP_400_BAD_REQUEST)

            activity.schedule=request.data['schedule']
            activity.save()
            activity_serializer = ActivitySerializers(activity)
            return Response(data=activity_serializer.data,status=HTTP_200_OK)
        except Exception as e:
            dataEx = {
                "msg" : e
            }
            return Response(data=dataEx,status=HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self,request, pk=None):
        try:
            activity = Activity.objects.get(pk=pk)
            if StatusEnum(activity.status) is StatusEnum.DEACTIVATE:
                dataR = {
                    "msg" : "Actividad ya está DESACTIVADA"
                }
                return Response(data=dataR,status=HTTP_400_BAD_REQUEST)

            activity.status=StatusEnum.DEACTIVATE.value
            activity.save()
            return Response(status=HTTP_204_NO_CONTENT)
        except Exception as e:
            dataEx = {
                "msg" : e
            }
            return Response(data=dataEx,status=HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request,pk=None):
        try:
            activity = Activity.objects.get(pk=pk)
            if StatusEnum(activity.status) is StatusEnum.ACTIVE \
                and activity.schedule >= now():
                condition = "Pendiente a realizar"
            elif StatusEnum(activity.status) is StatusEnum.ACTIVE \
                and activity.schedule < now():
                condition = "Atrasada"
            elif StatusEnum(activity.status) is StatusEnum.DONE:
                condition = "Finalizada"
            else:
                condition = activity.status
            
            dataSurvey = {
                "url" : "127.0.0.1:8000/api/survey/{}/".format(activity.id)
            }


            dataProperty = {
                "ID" : activity.property_id.id,
                "title" : activity.property_id.title,
                "address" : activity.property_id.address
            }

            dataAct = {
                "ID" : activity.id,
                "schedule" : activity.schedule,
                "title" : activity.title,
                "created_at" : activity.created_at,
                "status" : activity.status,
                "condition" : condition,
                "property" : dataProperty,
                "survey" : dataSurvey
            }

            return Response(data=dataAct,status=HTTP_200_OK)
        except Exception as e:
            dataEx = {
                "msg" : e
            }
            return Response(data=dataEx,status=HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            try:
                if "status" in request.data:
                    activities = Activity.objects.filter(status=request.data['status'])
                elif "start_date" in request.data and "end_date" in request.data:
                    start_date = request.data['start_date'] if request.data['start_date'] is not None else (now()-timedelta(days=3))
                    end_date = request.data['end_date'] if request.data['end_date'] is not None else (now() + timedelta(weeks=2))
                    activities = Activity.objects.filter(schedule__range=(start_date,end_date))
                else:
                    activities = Activity.objects.filter(schedule__range=(now()-timedelta(days=3),now() + timedelta(weeks=2)))
            except ValidationError as ve:
                dataEx = {
                    "msg" : ve
                }
                return Response(data=dataEx,status=HTTP_400_BAD_REQUEST)
            
            dataR = []
            for activity in activities:
                if StatusEnum(activity.status) is StatusEnum.ACTIVE \
                    and activity.schedule >= now():
                    condition = "Pendiente a realizar"
                elif StatusEnum(activity.status) is StatusEnum.ACTIVE \
                    and activity.schedule < now():
                    condition = "Atrasada"
                elif StatusEnum(activity.status) is StatusEnum.DONE:
                    condition = "Finalizada"
                else:
                    condition = activity.status
                
                dataSurvey = {
                    "url" : "127.0.0.1:8000/api/survey/{}/".format(activity.id)
                }


                dataProperty = {
                    "ID" : activity.property_id.id,
                    "title" : activity.property_id.title,
                    "address" : activity.property_id.address
                }

                dataAct = {
                    "ID" : activity.id,
                    "schedule" : activity.schedule,
                    "title" : activity.title,
                    "created_at" : activity.created_at,
                    "status" : activity.status,
                    "condition" : condition,
                    "property" : dataProperty,
                    "survey" : dataSurvey
                }

                dataR.append(dataAct)
            return Response(data=dataR,status=HTTP_200_OK)
        except Exception as e:
            dataEx = {
                "msg" : e
            }
            return Response(data=dataEx,status=HTTP_500_INTERNAL_SERVER_ERROR)


class SurveyViewsets(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Survey.objects.all()
    serializer_class = SurveySerializers