from users.views import get_user
from users.views import get_ref_claim
from users.views import post_score
from users.views import post_tickets
from users.views import remove_score
from users.views import remove_tickets
from users.views import start_mining
from users.views import done_mining
from tasks.views import get_tasks
from tasks.views import done_tasks
from django.urls import path


urlpatterns = [
    path('get/user/', get_user),
    path('get/tasks/', get_tasks),
    path('get/ref_claim/', get_ref_claim),
    path('done/tasks/', done_tasks),
    path('add/score/', post_score),
    path('add/tickets/', post_tickets),
    path('remove/score/', remove_score),
    path('remove/tickets/', remove_tickets),
    path('start/mining/', start_mining),
    path('done/mining/', done_mining),
]
