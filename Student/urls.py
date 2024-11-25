from django.urls import path



from .views import StudentView, TopperView ,HaveCut_off, PassOrNot, HaveAvg, TeacherPerformance
from .views import ActiveStudent, StudentCountView, StudentByDept, StudentBySchool, StudentByTeacher 
from .views import DeptPerformance 


urlpatterns = [
    path('',StudentView.as_view(),name="Student View"),
    path('<int:rollno>',StudentView.as_view(), name="Student View"),

    path('top/', TopperView.as_view(), name="Topper View"),
    path('top/<int:scid>/',TopperView.as_view(),name="Topper view by schools"),

    path('have/<str:cutoff>/', HaveCut_off.as_view(), name='have_cut_off'),
    path('have/<str:nocutoff>/', HaveCut_off.as_view(), name='have_cut_off'),
    path('have/<str:cutoff>/<int:scid>/', HaveCut_off.as_view(), name='have_cut_off'),
    path('have/<str:nocutoff>/<int:scid>/', HaveCut_off.as_view(), name='have_cut_off'),

    path('pass/<str:spass>/', PassOrNot.as_view(), name='pass_or_not'),
    path('pass/<str:spass>/<int:scid>/', PassOrNot.as_view(), name='pass_or_not'),

    path('avg/<str:avg>/',HaveAvg.as_view(), name='have_avg'),
    path('avg/<str:avg>/<int:scid>/', HaveAvg.as_view(), name='have_avg'),
    path('teacherperformance/', TeacherPerformance.as_view(), name='teacher_performance'),

    path('active/<str:active>/', ActiveStudent.as_view(), name='active_student'),
    path('active/<str:active>/<int:rollno>/', ActiveStudent.as_view(), name='active_student'),
    path('count/', StudentCountView.as_view(), name='student_count'),
    path('studentbydept/<int:deptid>/<int:scid>',StudentByDept.as_view(), name='student_by_dept'),
    path('studentbydept/<int:deptid>', StudentByDept.as_view(), name='student_by_dept'),
    path('studentbyschool/<int:schoolid>', StudentBySchool.as_view(), name='student_by_school'),
    path('studentbyschool/<str:name>', StudentBySchool.as_view(), name='student_by_school'),
    path('studentbyteacher/<int:teacherid>', StudentByTeacher.as_view(), name='student_by_teacher'),

    path('deptperformance/<int:scid>',DeptPerformance.as_view(), name='dept_performance'),
    
    
]