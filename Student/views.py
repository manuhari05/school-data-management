# these are the rest_framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

# these are django imports
from django.db.models import Sum ,Avg ,Count, Q

# these are local imports
from .models import Students
from .serializers import StudentsSerializer
from Teacher.models import Teachers
from .utils import calculate_passing_percentage
from Department.models import Departments
from School.models import Schools



# Create your views here.
'''
This is the StudentView class which is used to handle the CRUD operations on the Student model.
'''

class StudentView(APIView):

    
    '''
    this method is used to get the student data based on the rollno and retrieve all the students data

    Accepts:
        - rollno (optional):int datatype
    Returns:
        - 200 OK: List of students or student data in JSON format
        - 404 NOT FOUND: Error message if student data is not found


    '''
    def get(self, request, rollno=None):
        if rollno is not None:
            try:
                student = Students.objects.get(rollno=rollno)
                serializer = StudentsSerializer(student)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Students.DoesNotExist:
                return Response({"error": "Student Data not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            students = Students.objects.all()
            serializer = StudentsSerializer(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

    '''
    this method is used to craete and add new student to the database

    Accepts:
        - request.data: JSON object containing student information
    Returns:
        - 201 CREATED: Created student data in JSON format
        - 400 BAD REQUEST: Error message if validation fails

    '''
    
    def post(self, request):
        serialize=StudentsSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)
    
    '''
    this method is used to update the student data based on the rollno

     Accepts:
        - rollno: int datatype
        - request.data: JSON object containing updated student information (The JSON object should contain all manditary fields
        like :
            name, 
            teacher_id,
            maths_marks,
            physics_marks,
            chemistry_marks,
            )
    Returns:
        - 202 ACCEPTED: Updated student data in JSON format
        - 404 NOT FOUND: Error message if student data is not found
        - 400 BAD REQUEST: Error message if validation fails
    '''
  
        
    def put(self, request, rollno):
        try:
            student=Students.objects.get(rollno=rollno)
        except Students.DoesNotExist:
            return Response({"Message": "Sorry Given Provided Roll NUmber is not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=StudentsSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    

    ''' 
    this method is used to update the student data partially based on the rollno

    Accepts:
        - rollno:  int datatype
        - request.data: JSON object containing fields to update (partial data) ie., which / which are the fields need to updated
        like :
            name,
            teacher_id,
            maths_marks,
            physics_marks,
            chemistry_marks,
            )
    Returns:
        - 202 ACCEPTED: Updated student data in JSON format
        - 404 NOT FOUND: Error message if student data is not found
        - 400 BAD REQUEST: Error message if validation fails

    '''

    def patch(self, request, rollno):
        try:
            student=Students.objects.get(rollno=rollno)
        except Students.DoesNotExist:
            return Response({"Message": "Sorry Given Provided Roll NUmber is not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=StudentsSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    


    '''
    this method is used to delete the student data based on the rollno

    Accepts:
        - rollno: int dtatype
    Returns:
        - 204 NO CONTENT: Success message indicating data deletion
        - 404 NOT FOUND: Error message if student data is not found

    '''
    
    def delete(self, request, rollno):
        try:
            student=Students.objects.get(rollno=rollno)
        except Students.DoesNotExist:
            return Response({"Message": "Sorry Given Provided Roll NUmber is not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        student.delete()
        return Response({"Sucess": "Data Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)



'''
This is the TopperView class which is used to get the topper of the class based on the total marks
Accepts:
    - request: API request
    - scid (optional): int 
Returns:
    - 200 OK: List of top 5 students in JSON format
    - 404 NOT FOUND: Error message if school data is not found


'''

class TopperView(APIView):
    def get(self, request,scid=None):
        if scid is not None:
            try:
                #school=Schools.objects.get(id=scid)
                topper=Students.objects.filter(school__scid=scid).order_by('-total_marks')[:5]
                serializer=StudentsSerializer(topper, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Schools.DoesNotExist:
                return Response({"error": "School Data not found."}, status=status.HTTP_404_NOT_FOUND)
        topper=Students.objects.order_by('-total_marks')[:5]
        serializer=StudentsSerializer(topper,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


'''
This is the HaveCut_off class which is used to get the students who have the cutoff or not
Accepts:
    - request: API Request 
    - cutoff: str (either "cutoff" or "nocutoff")
    - scid (optional): int
Returns:
    - 200 OK: List of students meeting the cutoff criteria in JSON format
'''
    
class HaveCut_off(APIView):
    def get(self, request,cutoff,scid=None):
        if scid is not None:
            try:
                if cutoff=="cutoff":
                    topper=Students.objects.filter(school__scid=scid,total_marks__gte=calculate_passing_percentage())
                    serializer=StudentsSerializer(topper, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                elif cutoff=="nocutoff":
                    topper=Students.objects.filter(school__scid=scid, total_marks__lte=calculate_passing_percentage())
                    serializer=StudentsSerializer(topper, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Schools.DoesNotExist:
                return Response({"error": "School Data not found."}, status=status.HTTP_404_NOT_FOUND)

        if cutoff=="cutoff":
            topper=Students.objects.filter(total_marks__gte=calculate_passing_percentage())
            serializer=StudentsSerializer(topper, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif cutoff=="nocutoff":
            topper=Students.objects.filter(total_marks__lte=calculate_passing_percentage())
            serializer=StudentsSerializer(topper, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
'''
This is the PassOrNot class which is used to get the students who have passed or not based on the spass parameter,
where spass can be pass or notpass

Accepts:
    - request: API Request 
    - spass: str (either "pass" or "notpass")
   
    - scid (optional): int 
Returns:
    - 200 OK: List of students data in JSON format
    - 404 NOT FOUND: Error message if school data is not found
'''
    
class PassOrNot(APIView):
    def get(self, request,spass,scid=None, ):
        
        # if rollno is not None:
        #     student=Students.objects.get(rollno=rollno)
        #     serializer=StudentsSerializer(student)
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        if scid is not None:
            try:
                if spass=="pass":
                    student=Students.objects.filter(school__scid=scid, result=True)
                    serializer=StudentsSerializer(student, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                elif spass=="notpass":
                    student=Students.objects.filter(school__scid=scid, result=False)
                    serializer=StudentsSerializer(student, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Schools.DoesNotExist:
                return Response({"error": "School Data not found."}, status=status.HTTP_404_NOT_FOUND)
            
        if spass=="pass":
            student=Students.objects.filter(result=True)
            serializer=StudentsSerializer(student, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif spass=="notpass":
            student=Students.objects.filter(result=False)
            serializer=StudentsSerializer(student, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
'''
This is the HaveAvg class which is used to get the students who have the average marks or not based on the avg parameter,
where avg can be avg or noavg

Accepts:
    - request: API Request 
    - avg: str (either "avg" or "noavg")
    - scid (optional): int 
Returns:
    - 200 OK: List of students data in JSON format
    - 404 NOT FOUND: Error message if school data is not found

'''

class HaveAvg(APIView):
    def get(self,requset, avg,scid=None):
        total_avg_marks = Students.objects.aggregate(total=Avg('total_marks'))['total'] 
        

        # if rollno is not None:
        #     student=Students.objects.get(rollno=rollno)
        #     serializer=StudentsSerializer(student)
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        if scid is not None:
            try:
                if avg=="avg":
                    student=Students.objects.filter(school__scid=scid, total_marks__gte=total_avg_marks)
                    serializer=StudentsSerializer(student, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                elif avg=="noavg":
                    student=Students.objects.filter(school__scid=scid, total_marks__lte=total_avg_marks)
                    serializer=StudentsSerializer(student, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Schools.DoesNotExist:
                return Response({"error": "School Data not found."}, status=status.HTTP_404_NOT_FOUND)


        if avg=="avg":
            student=Students.objects.filter(total_marks__gte=total_avg_marks)
            serializer=StudentsSerializer(student, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif avg=="noavg":
            student=Students.objects.filter(total_marks__lte=total_avg_marks)
            serializer=StudentsSerializer(student, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
'''
This method retrieves performance for each teacher based on student results.
Accepts:
    - request: API Request
Returns:
    - 200 OK: Performance data of teachers and best teachers in JSON format
'''


class TeacherPerformance(APIView):
    def get(self, request):
        # Get distinct teacher IDs
        teachers = Teachers.objects.all()
        teacher_performance = []
        best_teachers = []
        high_pass = 0
        highpassing_percentage = 0

        for teacher in teachers:
            # Fetch students for the current teacher
            student_teacher = Students.objects.filter(teacher_id=teacher)
            total_students = student_teacher.count()
            passed_students = student_teacher.filter(result=True).count()
            avg_marks = student_teacher.aggregate(avg_marks=Avg('total_marks'))['avg_marks'] or 0


            passing_percentage = 0
            if total_students > 0:
                passing_percentage = (passed_students / total_students * 100)


            # Append performance data for the teacher
            teacher_performance.append({
                'teacher_id': teacher.empid,  # Assuming empid is the identifier
                'teacher_name': teacher.name,
                'total_students': total_students,
                'passed_students': passed_students,
                'avg_marks': avg_marks,
                'passing_percentage': passing_percentage,
            })

            # Check if this teacher has the highest number of passed students
            if passing_percentage  > highpassing_percentage :
                highpassing_percentage = passing_percentage
                best_teachers = [teacher.name]  # Store teacher names as strings
            elif passing_percentage == highpassing_percentage:
                best_teachers.append(teacher.name)  # Add teacher name to the list

        response_data = {
            'performance': teacher_performance,
            'best_teachers': best_teachers,
            'Passing_Percent': highpassing_percentage
        }

        return Response(response_data, status=status.HTTP_200_OK)

'''
This is the ActiveStudent class which is used to get the active or inactive students based on the active parameter,
where active can be active or inactive
'''    

class ActiveStudent(APIView):
    '''
    This view handles requests to retrieve students based on their active status.

    Accepted :
        - GET: API request to Retrieve active or inactive students or a specific student by roll number.
        - active (str): A string that indicates the desired student status:
            - "active": Fetch all active students.
            - "inactive": Fetch all inactive students.
        - rollno (optional): int (The roll number of the specific student to retrieve)

    Responses:
        - 200 OK: Returns a list of active/inactive students or a specific student.
        - 404 Not Found: If a specific student is requested but does not exist or is inactive.
        - 400 Bad Request: If the 'active' parameter is invalid.
    '''
    def get(self, request,active,rollno=None):
        if rollno is not None:
            try:
                student = Students.active.get_queryset().get(rollno=rollno)
                serializer = StudentsSerializer(student)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Students.DoesNotExist:
                raise NotFound(detail="Student not found or inactive.")
        
        if active == "active":
            active_students = Students.active.get_active()
            serializer = StudentsSerializer(active_students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif active == "inactive":
            inactive_students = Students.active.get_inactive()
            serializer = StudentsSerializer(inactive_students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "Invalid parameter."}, status=status.HTTP_400_BAD_REQUEST)
    
'''
This is the StudentCountView class which is used to get the count of active, inactive, and total students
'''
class StudentCountView(APIView):

    '''
    This method retrieves the count of active, inactive, and total students.

    Accepted :
        - GET: API request to Retrieve the count of active, inactive, and total students.

    Responses:
        - 200 OK: Returns a dictionary containing the count of active, inactive, and total students.
    '''
    def get(self, request):
        total_count = Students.objects.aggregate(
                                                  total_students=Count('rollno'),
                                                  active_students=Count('rollno',filter=Q(is_active=True)),
                                                  inactive_students=Count('rollno',filter=Q(is_active=False)),
                                                  )

        return Response(total_count, status=status.HTTP_200_OK)


'''
This StudentByDept is used to get the students who are belong the particular department
'''
class StudentByDept(APIView):
    '''
    This method is used to retrieve students based on the department ID or department name.

    Accepts:
        - deptid (int): The primary key of the department
        - scid (optional, int): The school ID
    Returns:
        - 200 OK: List of students belonging to the specified department in JSON format
        - 404 NOT FOUND: Error message if the department is not found or if no students are found
        - 400 BAD REQUEST: Error message if the department ID is invalid
    '''
    def get(self, request, deptid=0, scid=None):
        
            
        if deptid == 0:
            return Response({"error": "Invalid department ID."}, status=status.HTTP_400_BAD_REQUEST)
        
        if scid is not None:
            students=Students.objects.filter(dept=deptid,school=scid)
            if students.exists():
                serializer = StudentsSerializer(students, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "No students found for the specified department."}, status=status.HTTP_404_NOT_FOUND)
        
        elif deptid!=0:
            students=Students.objects.filter(dept=deptid)
            if students.exists():
                serializer = StudentsSerializer(students, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "No students found for the specified department."}, status=status.HTTP_404_NOT_FOUND)
        


        # students = Students.objects.filter(dept=deptid)
        
    
'''
This class is used to retrieve the students based on the school they are belong to

'''

class StudentBySchool(APIView):
    '''
    This method is used to retrieve students based on the school ID or school name.

    Accepts:
        - schoolid (int): The primary key of the school
        - name (optional, str): The name of the school
    Returns:
        - 200 OK: List of students belonging to the specified school in JSON format
        - 404 NOT FOUND: Error message if the school is not found or if no students are found
        - 400 BAD REQUEST: Error message if the school ID is invalid
    '''
    def get(self, request, schoolid=0, name=None):
        if name is not None:
            try:
                # school = Schools.objects.get(name=name)
                # Get all departments associated with the school
                # departments = Departments.objects.filter(school__name=name)
                # if not departments.exists():
                #     return Response({"error": "No departments found for the specified school."}, status=status.HTTP_404_NOT_FOUND)
                
                # Retrieve students from all departments of the school
                students = Students.objects.filter(school__name=name)
                serializer = StudentsSerializer(students, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Schools.DoesNotExist:
                return Response({"error": "School not found."}, status=status.HTTP_404_NOT_FOUND)

        if schoolid == 0:
            return Response({"error": "Invalid school ID."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # school = Schools.objects.get(scid=schoolid)
            # Get all departments associated with the school
            # departments = Departments.objects.filter(school__scid=schoolid)
            # if not departments.exists():
            #     return Response({"error": "No departments found for the specified school."}, status=status.HTTP_404_NOT_FOUND)
            
            # Retrieve students from all departments of the school
            students = Students.objects.filter(school__scid=schoolid)
            if students.exists():
                serializer = StudentsSerializer(students, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "No students found for the specified school."}, status=status.HTTP_404_NOT_FOUND)
        
        except Schools.DoesNotExist:
            return Response({"error": "School not found."}, status=status.HTTP_404_NOT_FOUND)


'''
This StudentByTeacher is used to get the students based on the teacher id
'''
class StudentByTeacher(APIView):
    '''
    This method is used to retrieve students based on the teacher ID.

    Accepts:
        - GET: API request to Retrieve students based on the teacher ID.
        - teacherid (int): The primary key of the teacher

    Responses:
        - 200 OK: List of students belonging to the specified teacher in JSON format
        - 404 NOT FOUND: Error message if the teacher is not found or if no students are found
        - 400 BAD REQUEST: Error message if the teacher ID is invalid
    '''
    def get(self, request, teacherid):
        try:
            # teacher = Teachers.objects.get(empid=teacherid)
            students = Students.objects.filter(teacher_id__empid=teacherid)
            if students.exists():
                serializer = StudentsSerializer(students, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "No students found for the specified teacher."}, status=status.HTTP_404_NOT_FOUND)
        except Teachers.DoesNotExist:
            return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

        

'''
This DeptPerformance class id used to calculate the department performance based the number of students
passed in the department and the total number of students in the department
'''


class DeptPerformance(APIView):

    '''
        This method is used to retrieve the performance of departments based on the number of students passed and the total number of students.

        Accepts:
            - GET: API request to Retrieve the performance of departments.
            - scid (int): The primary key of the school

        Responses:
            - 200 OK: List of departments with their performance data in JSON format.
        '''
   
    def get(self, request, scid):

        school=Schools.objects.get(scid=scid)
        
        performance={}

        for dept in school.dept.all():
            total_students = Students.objects.filter(dept=dept).count()
            passed_students = Students.objects.filter(dept=dept, result=True).count()
            if total_students == 0:
                percentage = 0
            else:
                percentage = (passed_students / total_students) * 100

            performance[dept.name] = {
                'total_students': total_students,
                'passed_students': passed_students,
                'percentage': percentage
            }

        return Response(performance, status=status.HTTP_200_OK)

        
