from rest_framework.test import APITestCase
from rest_framework import status
from apiREST.models import Property
from apiREST.models import Activity
import pytest


class ActivityTests(APITestCase):
    """
        Pruebas para el CRUD de Activity
    """    
    @pytest.mark.django_db
    def test_create_activity(self):
        """
            Método para testear la creación de una Activity
        """

        p = Property.objects.create(title="Propiedad prueba 01",address="Direccion prueba 01",description="Descripción prueba 01")
        
        url_activity = "/api/activity/"
        data = {
            "property_id" : p.id,
            "schedule" : "2022-01-04 15:49:13",
            "title" : "Activity de prueba"
        }
        response = self.client.post(url_activity,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(),1)

    @pytest.mark.django_db
    def test_list_activity(self):
        """
            Método para testear la lista de actividades
        """
        p = Property.objects.create(title="Propiedad prueba 01",address="Direccion prueba 01",description="Descripción prueba 01")
        url_activity = "/api/activity/"

        data = {
            "property_id" : p.id,
            "schedule" : "2022-01-04 17:49:13",
            "title" : "Activity de prueba"
        }
        response = self.client.post(url_activity,data,format='json')

        response = self.client.get(url_activity,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @pytest.mark.django_db
    def test_update_activity(self):
        """
            Método para testear update de activity
        """
        p = Property.objects.create(title="Propiedad prueba 01",address="Direccion prueba 01",description="Descripción prueba 01")
        url_activity = "/api/activity/"
        data = {
            "property_id" : p.id,
            "schedule" : "2022-01-04 17:49:13",
            "title" : "Activity de prueba"
        }
        response = self.client.post(url_activity,data,format='json')
        response = self.client.get(url_activity,format='json')
        
        
        newData = {
            "schedule" : "2022-01-04 20:00:00"
        }
        response = self.client.put(url_activity+str(response.data[0]['ID'])+"/",newData,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_delete_activity(self):
        """
            Método para delete la activity
        """

        p = Property.objects.create(title="Propiedad prueba 01",address="Direccion prueba 01",description="Descripción prueba 01")
        url_activity = "/api/activity/"
        data = {
            "property_id" : p.id,
            "schedule" : "2022-01-04 17:49:13",
            "title" : "Activity de prueba"
        }
        response = self.client.post(url_activity,data,format='json')
        response = self.client.get(url_activity,format='json')

        response = self.client.delete(url_activity+str(response.data[0]['ID'])+"/",format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)