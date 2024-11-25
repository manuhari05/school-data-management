from django.urls import path


from .views import DepartmentView, ActiveDept, DeprCountView

urlpatterns = [

    path('',DepartmentView.as_view(),name="Department View"),
    path('<int:deptid>',DepartmentView.as_view(), name="Department View"),
    path('active/<str:active>', ActiveDept.as_view(), name="Active Department"),
    path('active/<str:active>/<int:deptid>', ActiveDept.as_view(), name="Active Department"),
    path('count', DeprCountView.as_view(), name="Department Count"),
    # path('deptbyschool/<int:scid>',DeptBySchool.as_view(), name="Department By School"),
    # path('deptbyschool/<str:name>', DeptBySchool.as_view(), name="Department By School"),

    
]