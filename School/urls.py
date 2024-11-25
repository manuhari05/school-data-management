from django.urls import path


from .views import SchoolView, ActiveSchool, SchoolCountView, DeptINSchool

urlpatterns = [

    path('',SchoolView.as_view(),name="School View"),
    path('<int:scid>',SchoolView.as_view(), name="School View"),
    path('active/<str:active>', ActiveSchool.as_view(), name="Active School"),
    path('active/<str:active>/<int:scid>', ActiveSchool.as_view(), name="Active School"),
    path('count',SchoolCountView.as_view(), name="School Count"),
    path('count/<str:active>', SchoolCountView.as_view(), name="School Count"),
    path('dept/<int:scid>', DeptINSchool.as_view(), name="Department in School"),
    path('dept/<str:name>', DeptINSchool.as_view(), name="Department in School")

    
]