import config
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path(config.WEB_HOOK, views.web_hook, name='web_hook'),
]
