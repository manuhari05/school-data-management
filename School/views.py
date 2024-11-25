# these are the rest_framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

# these are local imports
from .models import Schools
from .serializers import SchoolSerializer
from Department.serializers import DepartmentSerializer




# Create your views here.
'''
This class is used to perform CRUD operations on the Schools table, where scid is the primary key.
'''


class SchoolView(APIView):

    '''
    This method is used to get the school data based on the scid and retrieve all school data.

    Accepts:
        - scid (optional): int datatype
    Returns:
        - 200 OK: List of schools or school data in JSON format
        - 404 NOT FOUND: Error message if school data is not found
    '''

    def get(self, request, scid=None):
        if scid is not None:
            try:
                schools = Schools.objects.get(scid=scid)
                serializer = SchoolSerializer(schools)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Schools.DoesNotExist:
                return Response({"error": "School Data not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            schools = Schools.objects.all()
            serializer = SchoolSerializer(schools, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    '''
    This method is used to create a new school record in the database.

    Accepts:
        - request.data: JSON object containing school information
    Returns:
        - 201 CREATED: Created school data in JSON format
        - 400 BAD REQUEST: Error message if validation fails
    '''
    
    def post(self, request):
        serialize=SchoolSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)
     
    '''
    This method is used to update an existing school record in the database.

    Accepts:
        - scid (int): The primary key of the school to update
        - request.data: JSON object containing updated school information
    Returns:
        - 202 ACCEPTED: Updated school data in JSON format
        - 404 NOT FOUND: Error message if school data is not found
        - 400 BAD REQUEST: Error message if validation fails
    '''
        
    def put(self, request, scid):
        try:
            schools=Schools.objects.get(scid=scid)
        except Schools.DoesNotExist:
            return Response({"Message": "Sorry Given Provided SCID is not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=SchoolSerializer(schools, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    

    '''
    This method is used to partially update an existing school record in the database.

    Accepts:
        - scid (int): The primary key of the school to update
        - request.data: JSON object containing the fields to update
    Returns:
        - 202 ACCEPTED: Updated school data in JSON format
        - 404 NOT FOUND: Error message if school data is not found
        - 400 BAD REQUEST: Error message if validation fails
    '''

    def patch(self, request, scid):
        try:
            schools=Schools.objects.get(scid=scid)
        except Schools.DoesNotExist:
            return Response({"Message": "Sorry Given Provided SCID is not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=SchoolSerializer(schools, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    '''
    This method is used to delete a school record from the database.

    Accepts:
        - scid (int): The primary key of the school to delete
    Returns:
        - 204 NO CONTENT: Confirmation that the school was deleted successfully
        - 404 NOT FOUND: Error message if school data is not found
    '''
    
    def delete(self, request, scid):
        try:
            schools=Schools.objects.get(scid=scid)
        except Schools.DoesNotExist:
            return Response({"Message": "Sorry Given Provided SCID is not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        schools.delete()
        return Response({"Sucess": "Data Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
    

'''
This is the ActiveSchool class which is used to get the active or inactive schools based on the active parameter,
where active can be active or inactive
'''    

class ActiveSchool(APIView):
    '''
    This view handles requests to retrieve schools based on their active status.

    Accepted :
        - GET: API request to Retrieve active or inactive schools or a specific school by scid.
        - active (str): A string that indicates the desired school status:
            - "active": Fetch all active schools.
            - "inactive": Fetch all inactive schools.
        - scid (optional): int (The scid of the specific school to retrieve)

    Responses:
        - 200 OK: Returns a list of active/inactive schools or a specific school.
        - 404 Not Found: If a specific school is requested but does not exist or is inactive.
        - 400 Bad Request: If the 'active' parameter is invalid.
    '''

    def get(self, request,active,scid=None):
        if scid is not None:
            try:
                student = Schools.active.get_queryset().get(scid=scid)
                serializer = SchoolSerializer(student)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Schools.DoesNotExist:
                raise NotFound(detail="School not found or inactive.")
        
        if active == "active":
            active_students = Schools.active.get_active()
            serializer = SchoolSerializer(active_students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif active == "inactive":
            inactive_students = Schools.active.get_inactive()
            serializer = SchoolSerializer(inactive_students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "Invalid parameter."}, status=status.HTTP_400_BAD_REQUEST)

'''
This is the SchoolCountView class which is used to get the count of active or inactive schools and total schools

'''
class SchoolCountView(APIView):
    '''
    This view handles requests to retrieve the count of active or inactive schools and total schools.

    Accepted :
        - GET: API request to Retrieve the count of active or inactive schools and total schools.

    Responses:
        - 200 OK: Returns the count of active or inactive schools.
        - 400 Bad Request: If the 'active' parameter is invalid.

    '''

    def get(self, request, active=None):
        if active is None:
            count = Schools.objects.count()
            active_count=Schools.active.get_active().count()
            inactive_count=Schools.active.get_inactive().count()
            return Response({"total_count": count, "active_count": active_count, "inactive_count": inactive_count}, status=status.HTTP_200_OK)
        if active == "active":
            count = Schools.active.get_active().count()
        elif active == "inactive":
            count = Schools.active.get_inactive().count()
        else:
            return Response({"detail": "Invalid parameter."}, status=status.HTTP_400_BAD_REQUEST)
        
        total_schools = Schools.objects.count()

        return Response({active+" count": count,"total_school":total_schools}, status=status.HTTP_200_OK)



'''
This DeptInSchool class is used to retrive the departments under the school

'''
class DeptINSchool(APIView):
    def get(self, request, scid=0, name=None):
        '''
        This method is used to get the departments under the school based on the scid or name.

        Accepts:
            - scid : int datatype
            - name (optional): str datatype
        Response:
            - 200 OK: List of departments under the school
            - 400 BAD REQUEST: Error message if scid or name is not provided or invalid
        '''
        if name is not None:
            try:
                school = Schools.objects.get(name=name)
                dept = school.dept.all()
            except Schools.DoesNotExist:
                return Response({"Message": "School not found"}, status=status.HTTP_404_NOT_FOUND)
        
        elif scid != 0:
            try:
                school = Schools.objects.get(scid=scid)
                dept = school.dept.all()
            except Schools.DoesNotExist:
                return Response({"Message": "School not found"}, status=status.HTTP_404_NOT_FOUND)
        
        else:
            return Response({"Message": "Please Provide Proper SCID or Name"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Serialize the department data
        serializer = DepartmentSerializer(dept, many=True)
        return Response( serializer.data, status=status.HTTP_200_OK)