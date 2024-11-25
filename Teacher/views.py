
# these are the rest_framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

# these are local imports
from .models import Teachers
from .serializers import TeacherSerializer
from Department.models import Departments
from School.models import Schools



# Create your views here.

'''
This is the TeacherView class which is used to handle the CRUD operations on the Teacher model.

'''

class TeacherView(APIView):


    '''
    this method is used to get the teacher data based on the empid and retrieve all the teachers data

    Accepts:
        - request: API Request 
        - empid (optional): int 
    Returns:
        - 200 OK: Teacher data or list of teachers in JSON format
        - 404 NOT FOUND: Error message if teacher data is not found

    '''

    def get(self, request, empid=None):
        
        if empid is not None:
            try:
                teacher = Teachers.objects.get(empid=empid)
                serializer = TeacherSerializer(teacher)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Teachers.DoesNotExist:
                return Response({"error": "Teacher Data not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            teachers = Teachers.objects.all()
            serializer = TeacherSerializer(teachers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

    '''
    this method is used to craete and add new teacher to the database
    Accepts:
        - request: API Request containing teacher data in JSON format with all the required field ie., empid and name
    Returns:
        - 201 CREATED: Created teacher data in JSON format
        - 400 BAD REQUEST: Error message if validation fails

    '''
        

    def post(self, request):
        serialize = TeacherSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    

    '''
    this method is used to update the teacher data based on the empid
     Accepts:
        - request: API Request containing updated teacher data in JSON format with all mandatory fields 
        - empid:int
    Returns:
        - 202 ACCEPTED: Updated teacher data in JSON format
        - 404 NOT FOUND: Error message if teacher data is not found
        - 400 BAD REQUEST: Error message if validation fails
    '''
    

    def put(self, request, empid):
        try:
            teacher = Teachers.objects.get(empid=empid)
        except Teachers.DoesNotExist:
            return Response({"Message": "Sorry Given Provided Empid is not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    

    '''
    this method is used to update the teacher data partially based on the empid

    Accepts:
        - request: API Request containing partial teacher data in JSON format
        - empid: int
    Returns:
        - 202 ACCEPTED: Updated teacher data in JSON format
        - 404 NOT FOUND: Error message if teacher data is not found
        - 400 BAD REQUEST: Error message if validation fails
    '''


    def patch(self, request, empid):
        try:
            teacher = Teachers.objects.get(empid=empid)
        except Teachers.DoesNotExist:
            return Response({"Message": "Sorry Given Provided Empid is not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    

    '''
    this method is used to delete the teacher data based on the empid
    Accepts:
        - request: API Request object
        - empid: int
    Returns:
        - 204 NO CONTENT: Success message indicating data deletion
        - 404 NOT FOUND: Error message if teacher data is not found
    '''
    

    def delete(self, request, empid):
        try:
            teacher = Teachers.objects.get(empid=empid)
        except Teachers.DoesNotExist:
            return Response({"Message": "Sorry Given Provided Empid is not exist"}, status=status.HTTP_404_NOT_FOUND)

        teacher.delete()
        return Response({"Sucess": "Data Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
    

'''
This is the ActiveTeacher class which is used to get the active or inactive teachers based on the active parameter,
where active can be active or inactive
'''    

class ActiveTeacher(APIView):
    '''
    This view handles requests to retrieve students based on their active status.

    Accepted :
        - GET: API request to Retrieve active or inactive teacher or a specific teacher by empid.
        - active (str): A string that indicates the desired teacher status:
            - "active": Fetch all active teachers.
            - "inactive": Fetch all inactive teachers.
        - empid (optional): int (The empid number of the specific student to retrieve)

    Responses:
        - 200 OK: Returns a list of active/inactive teachers or a specific Teacher.
        - 404 Not Found: If a specific teacher is requested but does not exist or is inactive.
        - 400 Bad Request: If the 'active' parameter is invalid.
    '''
    def get(self, request,active,empid=None):
        if empid is not None:
            try:
                student = Teachers.active.get_queryset().get(empid=empid)
                serializer = TeacherSerializer(student)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Teachers.DoesNotExist:
                raise NotFound(detail="Teacher not found or inactive.")
        
        if active == "active":
            active_students = Teachers.active.get_active()
            serializer = TeacherSerializer(active_students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif active == "inactive":
            inactive_students = Teachers.active.get_inactive()
            serializer = TeacherSerializer(inactive_students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "Invalid parameter."}, status=status.HTTP_400_BAD_REQUEST)

'''
This is the TeacherCountView class which is used to get the count of active, inactive, and total teachers

'''
class TeacherCountView(APIView):
    '''
    This view handles requests to retrieve the count of active, inactive and total teachers.

    Accepted :
        - GET: API request to Retrieve the count of active, inactive and total teachers.

    Responses:
        - 200 OK: Returns the count of active, inactive and total teachers.
    '''
    def get(self, request):
        active_count = Teachers.active.get_active().count()
        inactive_count = Teachers.active.get_inactive().count()
        total_count = Teachers.objects.count()
        return Response({"active_count": active_count, "inactive_count": inactive_count,"total_count": total_count}, status=status.HTTP_200_OK)
    

'''
This TeacherByDept class is used to get the teachers based on the department

'''
class TeacherByDept(APIView):
    '''
    This view handles requests to retrieve teachers based on their department.

    Accepted :
        - GET: API request to Retrieve teachers based on department.
        - dept (str): The department name for which to retrieve teachers.

    Responses:
        - 200 OK: Returns a list of teachers belonging to the specified department.
        - 400 Bad Request: If the 'dept' parameter is missing or invalid.
    '''
    def get(self, request, dept=0,scid=None):
        if dept==0:
            return Response({"error": "Invalid department ID."}, status=status.HTTP_400_BAD_REQUEST)
        
        if scid is not None :
            teachers = Teachers.objects.filter(dept=dept,school=scid)
            if not teachers.exists():
                return Response({"detail": "No teachers found for the specified department."}, status=status.HTTP_400_BAD_REQUEST)
            serializer = TeacherSerializer(teachers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif dept!=0:
            teachers = Teachers.objects.filter(dept=dept)
            if not teachers.exists():
                return Response({"detail": "No teachers found for the specified department."}, status=status.HTTP_400_BAD_REQUEST)
            serializer = TeacherSerializer(teachers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    
        

'''
This TeacherbySchool class is used to get the teachers based on the school

'''
class TeacherbySchool(APIView):
    '''
    This view handles requests to retrieve teachers based on their school.

    Accepted :
        - GET: API request to Retrieve teachers based on school.
        - school (str): The school name for which to retrieve teachers.

    Responses:
        - 200 OK: Returns a list of teachers belonging to the specified school.
        - 400 Bad Request: If the 'school' parameter is missing or invalid.
        - 404 Not Found: If no teachers are found for the specified school.
    '''
    def get(self, request,school=None):
        
        if school is not None:
            try:
                # schools = Schools.objects.get(scid=school)
                # Get all departments associated with the school
                # departments = Departments.objects.filter(school__scid=school)
                # if not departments.exists():
                #     return Response({"error": "No departments found for the specified school."}, status=status.HTTP_404_NOT_FOUND)
                
                # Retrieve students from all departments of the school
                teachers = Teachers.objects.filter(school=school,)
                if teachers.exists():
                    serializer = TeacherSerializer(teachers, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"error": "No teachers found for the specified school."}, status=status.HTTP_404_NOT_FOUND)
            
            except Schools.DoesNotExist:
                return Response({"error": "School not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"error": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)



        

