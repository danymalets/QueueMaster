from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bot', include('tg_bot.urls')),
    path('api', include('backend.urls')),
]
