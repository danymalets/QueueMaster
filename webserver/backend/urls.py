from django.urls import path
from . import views

urlpatterns = [
    path('get-user/<int:pk>', views.GetOrCreateUser.as_view()),
    path('save-user', views.SaveUser.as_view()),

    path('create-group', views.CreateGroup.as_view()),
    path('get-group/<int:pk>', views.GetGroup.as_view()),
    path('get-group-by-name/<str:name>', views.GetGroupByName.as_view()),
    path('save-group', views.SaveGroup.as_view()),

    path('get-queue/<int:pk>', views.GetQueue.as_view()),
    path('get-queue-by-name/<str:name>/<str:date>/<int:group>', views.GetQueueByName.as_view()),
    path('save-queue', views.SaveQueue.as_view()),
    path('create-queue', views.CreateQueue.as_view()),
]
