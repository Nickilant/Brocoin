from users.views import get_user
from tasks.views import get_tasks
from django.urls import path


urlpatterns = [
    path('get/user/', get_user),
    path('get/tasks/', get_tasks),

]
