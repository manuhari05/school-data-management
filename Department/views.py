# these are the rest_framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

# these are local imports
from .models import Departments
from .serializers import DepartmentSerializer
from School.models import Schools




# Create your views here.

'''
This class is used to perform CRUD operations on the Departments table, where deptid is the primary key
'''
class DepartmentView(APIView):
    '''
    Tthis method is used to get the department data based on the deptid and retrieve all the departments data

    Accepts:
        - deptid (optional):int datatype
    Returns:
        - 200 OK: List of departments or department data in JSON format
        - 404 NOT FOUND: Error message if department data is not found
    '''

    def get(self, request, deptid=None):
        if deptid is not None:
            try:
                department = Departments.objects.get(deptid=deptid)
                serializer = DepartmentSerializer(department)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Departments.DoesNotExist:
                return Response({"error": "Department Data not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            department = Departments.objects.all()
            serializer = DepartmentSerializer(department, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    '''
    This method is used to create a new department record in the database.

    Accepts:
        - request.data: JSON object containing department information
    Returns:
        - 201 CREATED: Created department data in JSON format
        - 400 BAD REQUEST: Error message if validation fails
    '''
        
    def post(self, request):
        serialize = DepartmentSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    
    '''
    This method is used to update an existing department record in the database.

    Accepts:
        - deptid (int): The primary key of the department to update
        - request.data: JSON object containing updated department information
    Returns:
        - 202 ACCEPTED: Updated department data in JSON format
        - 404 NOT FOUND: Error message if department data is not found
        - 400 BAD REQUEST: Error message if validation fails
    '''
    
    def put(self, request, deptid):
        try:
            department = Departments.objects.get(deptid=deptid)
        except Departments.DoesNotExist:
            return Response({"Message": "Sorry Given Provided Deptid is not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    '''This method is used to partially update an existing department record in the database.

    Accepts:
        - deptid (int): The primary key of the department to update
        - request.data: JSON object containing the fields to update
    Returns:
        - 202 ACCEPTED: Updated department data in JSON format
        - 404 NOT FOUND: Error message if department data is not found
        - 400 BAD REQUEST: Error message if validation fails
    '''

    def patch(self, request, deptid):
        try:
            department = Departments.objects.get(deptid=deptid)
        except Departments.DoesNotExist:
            return Response({"Message": "Sorry Given Provided Deptid is not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    

    '''
    This method is used to delete a department record from the database.

    Accepts:
        - deptid (int): The primary key of the department to delete
    Returns:
        - 204 NO CONTENT: Confirmation that the department was deleted successfully
        - 404 NOT FOUND: Error message if department data is not found
    '''
    

    def delete(self, request, deptid):
        try:
            department = Departments.objects.get(deptid=deptid)
        except Departments.DoesNotExist:
            return Response({"Message": "Sorry Given Provided Deptid is not exist"}, status=status.HTTP_404_NOT_FOUND)

        department.delete()
        return Response({"Sucess": "Data Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


'''
This is the ActiveDept class which is used to get the active or inactive departments based on the active parameter,
where active can be active or inactive
'''    

class ActiveDept(APIView):
    '''
    This view handles requests to retrieve departments based on their active status.

    Accepted :
        - GET: API request to Retrieve active or inactive departments or a specific student by deptid.
        - active (str): A string that indicates the desired department status:
            - "active": Fetch all active departments.
            - "inactive": Fetch all inactive departments.
        - deptid (optional): int (The deptid of the specific department to retrieve)

    Responses:
        - 200 OK: Returns a list of active/inactive departments or a specific Department.
        - 404 Not Found: If a specific department is requested but does not exist or is inactive.
        - 400 Bad Request: If the 'active' parameter is invalid.
    '''
    def get(self, request,active,deptid=None):
        if deptid is not None:
            try:
                student = Departments.active.get_queryset().get(deptid=deptid)
                serializer = DepartmentSerializer(student)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Departments.DoesNotExist:
                raise NotFound(detail="Department not found or inactive.")
        
        if active == "active":
            active_students = Departments.active.get_active()
            serializer = DepartmentSerializer(active_students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif active == "inactive":
            inactive_students = Departments.active.get_inactive()
            serializer = DepartmentSerializer(inactive_students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "Invalid parameter."}, status=status.HTTP_400_BAD_REQUEST)

'''
This is the DeprCountView class which is used to get the count of active, inactive and total departments

'''
class DeprCountView(APIView):
    '''
    This view handles requests to retrieve the count of active, inactive, and total departments.

    Accepted :
        - GET: API request to Retrieve the count of active, inactive, and total departments.

    Responses:
        - 200 OK: Returns a dictionary containing the count of active, inactive, and total departments.
    '''
    def get(self, request):
        active_count = Departments.active.get_active().count()
        inactive_count = Departments.active.get_inactive().count()
        total_count = Departments.active.get_queryset().count()

        count_data = {
            "active_count": active_count,
            "inactive_count": inactive_count,
            "total_count": total_count
        }

        return Response(count_data, status=status.HTTP_200_OK)
    

# '''
# This DeptBySchool class is used to get the departments based on the scid parameter and name parameter 
# '''
# class DeptBySchool(APIView):
#     '''
#     This view handles requests to retrieve departments based on the school they belong to.

#     Accepted :
#         - GET: API request to Retrieve departments based on the school they belong to.
#         - scid (int): The scid of the school to filter departments by.
#         - name (str): The name of the department to filter by (optional).

#     Responses:
#         - 200 OK: Returns a list of departments belonging to the specified school, filtered by name if provided.
#         - 404 Not Found: If no departments are found for the specified school or school does not exist.
#     '''
#     def get(self, request, scid=0, name=None):
#         if name is not None:
#             try:
#                 # schools = Schools.objects.get(name=name).scid # get the scid from the Schools
#                 departments = Departments.objects.filter(school__name=name)
#                 serializer = DepartmentSerializer(departments, many=True)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except Schools.DoesNotExist:
#                 return Response({"error": "School not found."}, status=status.HTTP_404_NOT_FOUND)
            
#         if scid == 0:
#             return Response({"error": "Invalid School ID."}, status=status.HTTP_400_BAD_REQUEST)

#         departments = Departments.objects.filter(school=scid)
#         if departments.exists():
#             serializer = DepartmentSerializer(departments, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response({"error": "No Department found for the specified School."}, status=status.HTTP_404_NOT_FOUND)
 
        