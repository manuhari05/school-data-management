from django.urls import path
from django.http import HttpResponse

from .views import UserView, LoginView

urlpatterns = [
    path('',UserView.as_view(),name='user_view'),
    path('user/<str:name>', UserView.as_view(), name='user_view'),
    path('login/', LoginView.as_view(), name='login_view'),

]