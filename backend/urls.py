import config
from django.urls import path
from . import views

urlpatterns = [
    path('getuser/<int:pk>', views.GetUser.as_view()),
    path('getgroup/<int:pk>', views.GetGroup.as_view()),
    path('getgroupbyname/<str:name>', views.GetGroupByName.as_view()),
    path('getqueue/<int:pk>', views.GetQueue.as_view()),
    path('saveuser', views.SaveUser.as_view()),
    path('savegroup', views.SaveGroup.as_view()),
    path('savequeue', views.SaveQueue.as_view()),
    path('creategroup', views.CreateGroup.as_view()),
    path('createqueue', views.CreateQueue.as_view()),
]
