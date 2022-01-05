# TestTrueHome
Test para TrueHome

https://apitruehomegeragg.herokuapp.com/api/activity/

api/activity/

  - Obtener Lista de Actividades 

    - GET   https://apitruehomegeragg.herokuapp.com/api/activity/

           - Filtros que se pueden aplicar

                {
                    "start_date" : "2022-01-04 17:49:13",
                    "end_date" : "2022-01-04 17:49:13"
                }
                
                {
                    "status" : "DEACTIVATE"
                }
          
    
  - Obtener Actividad por id

    - GET https://apitruehomegeragg.herokuapp.com/api/activity/:id/
    
  - Crear Actividad

    - POST  https://apitruehomegeragg.herokuapp.com/api/activity/

        {
            "property_id" : 1,
            "schedule" : "2022-01-04 15:49:13",
            "title" : "Activity de prueba"
        }
     
  - Actualizar Actividad

    - PUT https://apitruehomegeragg.herokuapp.com/api/activity/


        {
            "schedule" : "2022-01-04 20:00:00"
        }
    
