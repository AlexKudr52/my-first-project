from django.urls import path
from . import views

urlpatterns = [
    path('', views.Start_View, name='Start_View'),
    path('login', views.sign_in, name='login'),
    path('logout', views.sign_out, name='logout'),
    path('register', views.sign_up, name='register'),
    path('schedule', views.schedule, name='schedule'),
    path('confirm', views.confirm, name='confirm'),
    path('groupsone', views.groupsone, name='groupsone'),
    path('groupstwo', views.groupstwo, name='groupstwo'),
    path('groupsthree', views.groupsthree, name='groupsthree'),
]