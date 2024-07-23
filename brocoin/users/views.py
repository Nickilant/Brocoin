from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_user(request):
    cursor = connection.cursor()
    username = request.POST.get('username')
    #TODO От фронта надо получать поля username, user_id, ref_code
    cursor.execute(f"SELECT * FROM users where username = '{username}'")
    user = cursor.fetchall()
    cursor.execute(f"SELECT username, score, rank FROM (SELECT username, score, RANK() OVER (ORDER BY score DESC) AS rank FROM public.users) AS ranked_users WHERE username = '{username}'")
    rank = cursor.fetchall()
    print(rank)
    if user:
        answer = {
            'username': user[0][1],
            'score': user[0][2],
            'last_tap': str(user[0][3]),
            'referals': user[0][4],
            'ref_code': user[0][5],
            'position': rank[0][2],
        }
        return JsonResponse(answer)
    else:
        return JsonResponse({'error': 'user not exist'})


