from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connections, connection

class DistrictList(APIView):
    #Fetch District 
    def get(self, request):
        response = {}
        response['status'] = 0
        response['message'] = 'Data not found'
        response['data'] = { 'NULL' }
        sql_query = """ SELECT DISTINCT district FROM ap_mapping ; """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            district_data = cursor.fetchall()

        if district_data:
            response['status']  = 1
            response['message'] = 'Data fetched successfully'
            response['data']    = district_data
        else:
            response['status']  = 1
            response['message']   = 'Data not found'
            response['data']      = 'NULL'

        return Response(response, status=status.HTTP_200_OK)

class ACList(APIView):
    #Fetch  AC with corresponding District
    def post(self, request):
        response = {}
        response['status'] = 0
        response['message'] = 'Data not found'
        response['data'] = { 'NULL' }
        district = request.data.get('district')
        if not district:
            return Response({"error": "Please provide a valid district in the URL."}, status=400)
        
        sql_query = f"""SELECT DISTINCT ac FROM ap_mapping WHERE district = '{district}'; """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            ac_data = cursor.fetchall()
        
        if ac_data:
            response['status']  = 1
            response['message'] = 'Data fetched successfully'
            response['data']    = ac_data
        else:
            response['status']  = 1
            response['message']   = 'Data not found'
            response['data']      = 'NULL'
        
        # json_response = json.dumps(response)
        return Response(response, status=status.HTTP_200_OK)
 
class MandalList(APIView):
    # Fetch  Mandal with corresponding District, AC
    def post(self, request):
        response = {}
        response['status'] = 0
        response['message'] = 'Data not found'
        response['data'] = { 'NULL' }
        district = request.data.get('district')
        ac = request.data.get('ac')

        if not ac:
            return Response({"error": "Please provide a valid AC in the URL."}, status=400)
        # Fetch the data using the SQL query
        sql_query = f"""SELECT DISTINCT mandal FROM ap_mapping WHERE ac = '{ac}'AND district = '{district}'; """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            mandal_data = cursor.fetchall()

        if mandal_data:
            response['status']  = 1
            response['message'] = 'Data fetched successfully'
            response['data']    = mandal_data
        else:
            response['status']  = 1
            response['message']   = 'Data not found'
            response['data']      = 'NULL'
        
        # json_response = json.dumps(response)
        return Response(response, status=status.HTTP_200_OK)
    
class secretariatList(APIView):
    # Fetch secretariat with corresponding District, AC, secretariat
    def post(self, request): 
        response = {}
        response['status'] = 0
        response['message'] = 'Data not found'
        response['data'] = { 'NULL' }

        ac = request.data.get('ac')
        district = request.data.get('district')
        mandal = request.data.get('mandal')

        sql_query = f"""SELECT DISTINCT secreteriat FROM ap_mapping WHERE ac = '{ac}'AND district = '{district}'AND mandal = '{mandal}'; """

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            secretariat_data = cursor.fetchall()

        if secretariat_data:
            response['status']  = 1
            response['message'] = 'Data fetched successfully'
            response['data']    = secretariat_data
        else:
            response['status']  = 1
            response['message']   = 'Data not found'
            response['data']      = 'NULL'
        
        # json_response = json.dumps(response)
        return Response(response, status=status.HTTP_200_OK)

class Submit(APIView):
    def post(self, request):
        response = {}
        response['status'] = 0
        response['message'] = 'Data not found'
        response['data'] = { 'NULL' }

        booklet_no = request.data.get('booklet_no')
        agent_id = request.data.get('agent')
        ac = request.data.get('ac')
        ac_other = request.data.get('ac_other')
        district = request.data.get('district')
        district_other = request.data.get('district_other')
        mandal = request.data.get('mandal')
        mandal_other = request.data.get('mandal_other')
        village = request.data.get('village')
        ward = request.data.get('ward')
        ward_other = request.data.get('ward_other')
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')

        sql_query = f"""INSERT INTO form_submit (booklet_number, agent_id, district, district_other, ac, ac_other, mandal, mandal_other, village,  ward, ward_other, name, phone_number) 
                        VALUES ('{booklet_no}', '{agent_id}', '{district}', '{district_other}', '{ac}', '{ac_other}', '{mandal}', '{mandal_other}', '{village}', '{ward}', '{ward_other}', '{name}', '{phone_number}');
                    """
        my_connection = connections['secondary']
        with my_connection.cursor() as cursor:
            try:
                cursor.execute(sql_query)
                response['status'] = 1
                response['message'] = 'Data inserted successfully'
                response['data'] = None
            except Exception as e:
                response['status'] = 0
                response['message'] = f"Error occurred: {str(e)}"
                response['data'] = None

        return Response(response, status=status.HTTP_200_OK)
    