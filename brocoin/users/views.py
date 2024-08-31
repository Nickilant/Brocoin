from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from datetime import datetime, timedelta


@csrf_exempt
def get_user(request):
    """Получение данных по пользователю"""
    cursor = connection.cursor()
    username = request.POST.get('username')
    user_id = request.POST.get('user_id')
    ref_code = request.POST.get('ref_code')
    premium = request.POST.get('premium')
    #TODO От фронта надо получать поля username, user_id, ref_code
    cursor.execute(f"SELECT * FROM users where username = '{username}'")
    user = cursor.fetchall()
    if not user:
        refs = json.dumps({'id': []})
        cursor.execute(f"INSERT INTO public.users (sid,username,score,last_score,last_tap,ref_code,refs,energy,tickets,mining_claim) VALUES ('{uuid.uuid4()}','{username}',25,0,'{datetime.now()}','{user_id}',{repr(refs)},1000,25, True)")
        cursor.execute(f"INSERT INTO public.referals_score (username,score) VALUES ('{user_id}',0)")
        if ref_code:
            cursor.execute(f"SELECT refs, tickets, score FROM users WHERE ref_code='{ref_code}'")
            referals = cursor.fetchall()
            actual_refs = referals[0][0]
            actual_tickets = referals[0][1]
            actual_score = referals[0][2]
            actual_refs['id'].append(user_id)
            if not premium:
                cursor.execute(f"UPDATE users set refs='{json.dumps(actual_refs)}', tickets = {int(actual_tickets) + 1} where ref_code='{ref_code}'")
            else:
                cursor.execute(
                    f"UPDATE users set refs='{json.dumps(actual_refs)}', tickets = {int(actual_tickets) + 3}, score = {int(actual_score) + 50} where ref_code='{ref_code}'")
    cursor.execute(f"SELECT * FROM users where username = '{username}'")
    user = cursor.fetchall()

    if user:
        cursor.execute(
            f"SELECT username, score, rank FROM (SELECT username, score, RANK() OVER (ORDER BY score DESC) AS rank FROM public.users) AS ranked_users WHERE username = '{username}'")
        rank = cursor.fetchall()
        cursor.execute(f"SELECT * FROM users where username = '{username}'")
        user = cursor.fetchall()
        #-------------Вычисление времени таймера

        db_time_str = str(user[0][3])

        # Преобразуем строку в объект datetime
        db_time = datetime.strptime(db_time_str, "%Y-%m-%d %H:%M:%S.%f")

        # Получаем текущее время
        current_time = datetime.now()

        # Вычисляем разницу между текущим временем и временем из базы данных
        time_diff = current_time - db_time

        # Время, соответствующее 8 часам
        eight_hours = timedelta(hours=8)

        # Вычитаем разницу из 8 часов
        remaining_time = eight_hours - time_diff

        # Преобразуем оставшееся время в часы и минуты
        remaining_hours, remainder = divmod(remaining_time.total_seconds(), 3600)
        remaining_minutes, _ = divmod(remainder, 60)

        # Форматируем результат в HH:MM
        formatted_time = f"{int(remaining_hours):02}:{int(remaining_minutes):02}"

        #-----------------------------------
        answer_ref = []
        for i in user[0][4]['id']:
            cursor.execute(f"SELECT * FROM users where ref_code = '{i}'")
            ref = cursor.fetchall()
            cursor.execute(f"SELECT score FROM public.referals_score where username = '{i}'")
            ref_score = cursor.fetchall()
            bonus = 0
            if ref[0][5]:
                bonus = '5000'
            referal = {
                'username': ref[0][1],
                'refs': len(ref[0][4]['id']),
                'bonus': bonus,
                'reward': int(int(ref_score[0][0])/10),
            }
            answer_ref.append(referal)

        answer = {
            'username': user[0][1],
            'score': user[0][2],
            'left_mining': formatted_time if formatted_time > "0" else "00:00",
            'mining_claim': user[0][12],
            'referals': answer_ref,
            'ref_code': user[0][6],
            'position': rank[0][2],
            'tickets': user[0][11],

        }
        return JsonResponse(answer)
    else:
        return JsonResponse({'error': 'user not exist'})


@csrf_exempt
def get_ref_claim(request):
    """Сбор монет с рефералов"""
    try:
        cursor = connection.cursor()
        username = request.POST.get('username')
        cursor.execute(f"SELECT * FROM users where username = '{username}'")
        user = cursor.fetchall()
        score_up = 0
        for i in user[0][4]['id']:
            cursor.execute(f"SELECT * FROM public.referals_score where username = '{i}'")
            ref_score = cursor.fetchall()
            cursor.execute(f"UPDATE public.referals_score set score=0 where username = '{i}'")
            score_up += int(ref_score[0][1])
        cursor.execute(
            f"UPDATE public.users SET score = '{int(user[0][2]) + int((score_up / 10))}' where username = '{user[0][1]}'")
        return JsonResponse({'Claim': 'Complete'})
    except Exception as e:
        return JsonResponse({'Claim': f'Error: {e}'})


@csrf_exempt
def post_score(request):
    """Добавление очков"""
    cursor = connection.cursor()
    username = request.POST.get('username')
    user_score = request.POST.get('score')
    cursor.execute(f"SELECT * FROM users where username = '{username}'")
    user = cursor.fetchall()
    summ_score = int(user[0][2]) + int(user_score)
    cursor.execute(f"UPDATE users set score = {summ_score} where username = '{username}'")
    cursor.execute(f"SELECT * FROM users where username = '{username}'")
    user = cursor.fetchall()
    cursor.execute(f"SELECT * FROM public.referals_score where username = '{user[0][6]}'")
    referals_score = cursor.fetchall()
    cursor.execute(f"UPDATE referals_score set score = {int(referals_score[0][1])+int(user_score)} where username = '{user[0][6]}'")
    return JsonResponse({'Added': 'Complete'})


@csrf_exempt
def remove_score(request):
    """Добавление очков"""
    cursor = connection.cursor()
    username = request.POST.get('username')
    user_score = request.POST.get('score')
    cursor.execute(f"SELECT * FROM users where username = '{username}'")
    user = cursor.fetchall()
    summ_score = int(user[0][2]) - int(user_score)
    cursor.execute(f"UPDATE users set score = {summ_score} where username = '{username}'")
    return JsonResponse({'Remove': 'Complete'})


@csrf_exempt
def post_tickets(request):
    """Добавление тикетов"""
    cursor = connection.cursor()
    username = request.POST.get('username')
    user_tickets = request.POST.get('tickets')
    cursor.execute(f"SELECT * FROM users where username = '{username}'")
    user = cursor.fetchall()
    summ_tickets = int(user[0][11]) + int(user_tickets)
    cursor.execute(f"UPDATE users set tickets = {summ_tickets} where username = '{username}'")
    return JsonResponse({'Added': 'Complete'})


@csrf_exempt
def remove_tickets(request):
    """Добавление тикетов"""
    cursor = connection.cursor()
    username = request.POST.get('username')
    user_tickets = request.POST.get('tickets')
    cursor.execute(f"SELECT * FROM users where username = '{username}'")
    user = cursor.fetchall()
    summ_tickets = int(user[0][11]) - int(user_tickets)
    cursor.execute(f"UPDATE users set tickets = {summ_tickets} where username = '{username}'")
    return JsonResponse({'Remove': 'Complete'})

@csrf_exempt
def start_mining(request):
    """Установка временной метки начала майнинга"""
    username = request.POST.get('username')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE users set last_tap='{datetime.now()}', mining_claim = False where username='{username}'")
    return JsonResponse({'Mining': 'Start'})


@csrf_exempt
def done_mining(request):
    """Завершение майнинга"""
    username = request.POST.get('username')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM users where username = '{username}'")
    user = cursor.fetchall()
    summ_score = int(user[0][2]) + 72
    cursor.execute(f"UPDATE users set mining_claim = True, score = {summ_score} where username='{username}'")
    return JsonResponse({'Mining': 'Done'})




