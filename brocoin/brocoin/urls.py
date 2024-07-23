from users.views import start
from django.urls import path


urlpatterns = [
    path('get/user/', start)
]
