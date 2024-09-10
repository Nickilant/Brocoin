from users.views import get_user
from users.views import get_ref_claim
from users.views import post_score
from users.views import post_tickets
from users.views import remove_score
from users.views import remove_tickets
from users.views import start_mining
from users.views import done_mining
from users.views import get_referals
from users.views import done_daily
from users.views import done_first_login
from users.views import switch_region
from users.views import post_boxes
from users.views import advertising_see
from tasks.views import get_tasks
from tasks.views import done_tasks
from django.urls import path
from django.conf.urls import handler404
from tasks.views import custom_404

handler404 = custom_404


urlpatterns = [
    path('gets/user/', get_user),
    path('get/referals/', get_referals),
    path('get/tasks/', get_tasks),
    path('get/boxes/', post_boxes),
    path('get/ref_claim/', get_ref_claim),
    path('done/tasks/', done_tasks),
    path('add/score/', post_score),
    path('add/tickets/', post_tickets),
    path('remove/score/', remove_score),
    path('remove/tickets/', remove_tickets),
    path('start/mining/', start_mining),
    path('done/mining/', done_mining),
    path('done/daily/', done_daily),
    path('done/first_login/', done_first_login),
    path('switch_region/', switch_region),
    path('advertising_see/', advertising_see),
]
