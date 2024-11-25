from django.urls import path

from .views import TeacherView , ActiveTeacher, TeacherCountView, TeacherByDept, TeacherbySchool

urlpatterns = [
    path('',TeacherView.as_view(),name="Teacher View"),
    path('<int:empid>',TeacherView.as_view(), name="Teacher View"),
    path('active/<str:active>', ActiveTeacher.as_view(), name="Active Teacher"),
    path('active/<str:active>/<int:empid>', ActiveTeacher.as_view(), name="Active Teacher"),
    path('count/', TeacherCountView.as_view(), name="Teacher Count"),
    path('teacherbydept/<int:dept>', TeacherByDept.as_view(), name="Teacher By Department"),
    path('teacherbydept/<int:dept>/<int:scid>', TeacherByDept.as_view(), name="Teacher By Department"),
    path('teacherbyschool/<int:school>', TeacherbySchool.as_view(), name="Teacher By School"),

    
]