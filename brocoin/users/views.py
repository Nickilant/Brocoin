from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
import users.enums as dailyEnums
from datetime import datetime, timedelta, date
from django.core.paginator import Paginator
import random


@csrf_exempt
def get_user(request):
    """Получение данных по пользователю"""
    cursor = connection.cursor()
    username = request.POST.get('username')
    user_id = request.POST.get('user_id')
    ref_code = request.POST.get('ref_code')
    premium = request.POST.get('premium')
    cursor.execute(f"SELECT * FROM users where ref_code = '{user_id}'")
    user = cursor.fetchall()
    if not user:
        refs = json.dumps({'id': []})
        cursor.execute(f"INSERT INTO public.users (sid,username,score,last_score,last_tap,ref_code,refs,energy,tickets,mining_claim, last_login, reward_streak, region) VALUES ('{uuid.uuid4()}','{username}',25,0,'{datetime.now()}','{user_id}',{repr(refs)},1000,25, True, '{date.today()}',1, 'eng')")
        cursor.execute(f"INSERT INTO public.referals_score (username,score) VALUES ('{user_id}',0)")
        if ref_code:
            cursor.execute(f"SELECT refs, tickets, score FROM users WHERE ref_code='{ref_code}'")
            referals = cursor.fetchall()
            actual_refs = referals[0][0]
            actual_tickets = referals[0][1]
            actual_score = referals[0][2]
            actual_refs['id'].append(user_id)
            if not premium:
                cursor.execute(f"UPDATE users set refs='{json.dumps(actual_refs)}', tickets = {int(actual_tickets) + 3} where ref_code='{ref_code}'")
            else:
                cursor.execute(
                    f"UPDATE users set refs='{json.dumps(actual_refs)}', tickets = {int(actual_tickets) + 12}, score = {int(actual_score) + 50} where ref_code='{ref_code}'")
    cursor.execute(f"SELECT * FROM users where ref_code = '{user_id}'")
    user = cursor.fetchall()

    if user:
        cursor.execute(
            f"SELECT username, score, rank FROM (SELECT username, score, RANK() OVER (ORDER BY score DESC) AS rank FROM public.users) AS ranked_users WHERE username = '{username}'")
        rank = cursor.fetchall()
        cursor.execute(f"SELECT * FROM users where ref_code = '{user_id}'")
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
        # Проверяем дейлистрик-----------------------
        date_time = str(user[0][13])
        last_login = datetime.strptime(date_time, "%Y-%m-%d").date()
        today = date.today()
        yesterday = today - timedelta(days=1)
        if last_login == today:
            pass
        else:
            if last_login == yesterday:
                reward_streak = int(user[0][14])+1
                cursor.execute(
                    f"UPDATE public.users set last_login='{today}', reward_streak = {reward_streak} where ref_code='{user[0][6]}'")
                cursor.execute(f"UPDATE public.users set daily_claim=False, first_game=True,advertising_limit = 10 where ref_code = '{user[0][6]}' ")
            else:
                cursor.execute(
                    f"UPDATE public.users set last_login='{today}', reward_streak = {1} where ref_code='{user[0][6]}'")
                cursor.execute(f"UPDATE public.users set daily_claim=False, first_game=True,advertising_limit = 10 where ref_code='{user[0][6]}' ")
        # -------------------------------------------
        cursor.execute(f"SELECT * FROM users where ref_code='{user[0][6]}'")
        user = cursor.fetchall()
        answer = {
            'username': user[0][1],
            'score': user[0][2],
            'left_mining': formatted_time if formatted_time > "0" else "00:00",
            'mining_claim': user[0][12],
            'ref_code': user[0][6],
            'position': rank[0][2],
            'tickets': user[0][11],
            'boxes': user[0][18],
            'daily_stric': user[0][14],
            "daily_claim": user[0][15],
            "first_login": user[0][16],
            "region": user[0][17],
            "first_game": user[0][19],
            "advertising_limit": user[0][20],
            "advertising_total": 10,


        }
        return JsonResponse(answer)
    else:
        return JsonResponse({'error': 'user not exist'})


@csrf_exempt
def get_referals(request):
    """Получение рефералов пользователя с пагинацией"""
    cursor = connection.cursor()
    user_id = request.POST.get('user_id')
    page = int(request.POST.get('page', 1))  # текущая страница
    limit = int(request.POST.get('limit', 2))  # количество рефералов на странице

    cursor.execute(f"SELECT * FROM users WHERE ref_code = '{user_id}'")
    user = cursor.fetchall()
    total_score = 0
    for i in user[0][4]['id']:
        cursor.execute(f"SELECT * FROM public.referals_score where username = '{i}'")
        ref_score = cursor.fetchall()
        total_score += int(ref_score[0][1])
    #cursor.execute(f"SELECT SUM(score) AS total_score FROM referals_score where username = '{user_id}'")
    #total_score = cursor.fetchall()
    if not user:
        return JsonResponse({"error": "User not found"}, status=404)

    referal_ids = user[0][4]['id']  # список ID рефералов

    paginator = Paginator(referal_ids, limit)  # создаем пагинатор
    try:
        referal_page = paginator.page(page)
    except Exception as e:
        return JsonResponse({"error": "Page not found"}, status=404)

    answer_ref = []
    for i in referal_page.object_list:
        cursor.execute(f"SELECT * FROM users WHERE ref_code = '{i}'")
        ref = cursor.fetchall()

        cursor.execute(f"SELECT score FROM public.referals_score WHERE username = '{i}'")
        ref_score = cursor.fetchall()

        bonus = '5000' if ref[0][5] else 0

        referal = {
            'username': ref[0][1],
            'refs': len(ref[0][4]['id']),
            'bonus': bonus,
            'reward': int(int(ref_score[0][0]) / 10),
        }
        answer_ref.append(referal)

    answer = {
        'username': user[0][1],
        'referals': answer_ref,
        'total_referals': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page,
        'total_score': total_score/10,
    }
    return JsonResponse(answer)


@csrf_exempt
def done_daily(request):
    """Выполнение ежедневных тасок"""
    cursor = connection.cursor()
    # username = request.POST.get('username')
    user_id = request.POST.get('user_id')
    cursor.execute(f"SELECT reward_streak, score, tickets FROM users where ref_code = '{user_id}'")
    user = cursor.fetchall()
    cursor.execute(f"UPDATE public.users set daily_claim=True where ref_code = '{user_id}' ")
    if int(user[0][0]) == 1:
        cursor.execute(f"UPDATE public.users set score = {int(user[0][1]) + int(dailyEnums.DeyOne.POINTS)}, tickets = {int(user[0][2]) + int(dailyEnums.DeyOne.TICKETS)} where ref_code = '{user_id}' ")
    if int(user[0][0]) == 2:
        cursor.execute(f"UPDATE public.users set score = {int(user[0][1]) + int(dailyEnums.DeyTwo.POINTS)}, tickets = {int(user[0][2]) + int(dailyEnums.DeyTwo.TICKETS)} where ref_code = '{user_id}' ")
    if int(user[0][0]) == 3:
        cursor.execute(f"UPDATE public.users set score = {int(user[0][1]) + int(dailyEnums.DeyTree.POINTS)}, tickets = {int(user[0][2]) + int(dailyEnums.DeyTree.TICKETS)} where ref_code = '{user_id}' ")
    if int(user[0][0]) == 4:
        cursor.execute(f"UPDATE public.users set score = {int(user[0][1]) + int(dailyEnums.DeyFour.POINTS)}, tickets = {int(user[0][2]) + int(dailyEnums.DeyFour.TICKETS)} where ref_code = '{user_id}' ")
    if int(user[0][0]) == 5:
        cursor.execute(f"UPDATE public.users set score = {int(user[0][1]) + int(dailyEnums.DeyFive.POINTS)}, tickets = {int(user[0][2]) + int(dailyEnums.DeyFive.TICKETS)} where ref_code = '{user_id}' ")
    if int(user[0][0]) == 6:
        cursor.execute(f"UPDATE public.users set score = {int(user[0][1]) + int(dailyEnums.DeySix.POINTS)}, tickets = {int(user[0][2]) + int(dailyEnums.DeySix.TICKETS)} where ref_code = '{user_id}' ")
    if int(user[0][0]) >= 7:
        cursor.execute(f"UPDATE public.users set score = {int(user[0][1]) + int(dailyEnums.DeySeven.POINTS)}, tickets = {int(user[0][2]) + int(dailyEnums.DeySeven.TICKETS)} where ref_code = '{user_id}' ")
    print(user[0][0])
    return JsonResponse({'daily_claim': 'done'})


@csrf_exempt
def get_ref_claim(request):
    """Сбор монет с рефералов"""
    try:
        cursor = connection.cursor()
        # username = request.POST.get('username')
        user_id = request.POST.get('user_id')
        cursor.execute(f"SELECT * FROM users where ref_code = '{user_id}'")
        user = cursor.fetchall()
        score_up = 0
        for i in user[0][4]['id']:
            cursor.execute(f"SELECT * FROM public.referals_score where username = '{i}'")
            ref_score = cursor.fetchall()
            cursor.execute(f"UPDATE public.referals_score set score=0 where username = '{i}'")
            score_up += int(ref_score[0][1])
        cursor.execute(
            f"UPDATE public.users SET score = '{int(user[0][2]) + int((score_up / 10))}' where ref_code = '{user[0][6]}'")
        return JsonResponse({'Claim': 'Complete'})
    except Exception as e:
        return JsonResponse({'Claim': f'Error: {e}'})


@csrf_exempt
def post_score(request):
    """Добавление очков"""
    cursor = connection.cursor()
    response_text = {'Added': 'Complete'}
    # username = request.POST.get('username')
    user_id = request.POST.get('user_id')
    user_score = request.POST.get('score')
    cursor.execute(f"SELECT * FROM users where ref_code = '{user_id}'")
    user = cursor.fetchall()
    summ_score = int(user[0][2]) + int(user_score)
    cursor.execute(f"UPDATE users set score = {summ_score}, first_game=False where ref_code = '{user_id}'")
    if random.randint(1, 100) == 1:
        cursor.execute(f"UPDATE users set boxes = {int(user[0][18])+1} where ref_code = '{user_id}'")
        response_text = {'Added': 'Complete + box'}
    cursor.execute(f"SELECT * FROM users where ref_code = '{user_id}'")
    user = cursor.fetchall()
    cursor.execute(f"SELECT * FROM public.referals_score where username = '{user[0][6]}'")
    referals_score = cursor.fetchall()
    cursor.execute(f"UPDATE referals_score set score = {int(referals_score[0][1])+int(user_score)} where username = '{user[0][6]}'")
    return JsonResponse(response_text)


@csrf_exempt
def remove_score(request):
    """Удаление очков"""
    cursor = connection.cursor()
    # username = request.POST.get('username')
    user_id = request.POST.get('user_id')
    user_score = request.POST.get('score')
    cursor.execute(f"SELECT * FROM users where ref_code = '{user_id}'")
    user = cursor.fetchall()
    summ_score = int(user[0][2]) - int(user_score)
    cursor.execute(f"UPDATE users set score = {summ_score} where ref_code = '{user_id}'")
    return JsonResponse({'Remove': 'Complete'})


@csrf_exempt
def post_tickets(request):
    """Добавление тикетов"""
    cursor = connection.cursor()
    # username = request.POST.get('username')
    user_id = request.POST.get('user_id')
    user_tickets = request.POST.get('tickets')
    cursor.execute(f"SELECT * FROM users where ref_code = '{user_id}'")
    user = cursor.fetchall()
    summ_tickets = int(user[0][11]) + int(user_tickets)
    cursor.execute(f"UPDATE users set tickets = {summ_tickets} where ref_code = '{user_id}'")
    return JsonResponse({'Added': 'Complete'})


@csrf_exempt
def remove_tickets(request):
    """Добавление тикетов"""
    cursor = connection.cursor()
    # username = request.POST.get('username')
    user_id = request.POST.get('user_id')
    user_tickets = request.POST.get('tickets')
    cursor.execute(f"SELECT * FROM users where ref_code = '{user_id}'")
    user = cursor.fetchall()
    summ_tickets = int(user[0][11]) - int(user_tickets)
    cursor.execute(f"UPDATE users set tickets = {summ_tickets} where ref_code = '{user_id}'")
    return JsonResponse({'Remove': 'Complete'})

@csrf_exempt
def start_mining(request):
    """Установка временной метки начала майнинга"""
    # username = request.POST.get('username')
    user_id = request.POST.get('user_id')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE users set last_tap='{datetime.now()}', mining_claim = False where ref_code = '{user_id}'")
    return JsonResponse({'Mining': 'Start'})


@csrf_exempt
def done_mining(request):
    """Завершение майнинга"""
    # username = request.POST.get('username')
    user_id = request.POST.get('user_id')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM users where ref_code = '{user_id}'")
    user = cursor.fetchall()
    summ_score = int(user[0][2]) + 72
    cursor.execute(f"UPDATE users set mining_claim = True, score = {summ_score} where ref_code = '{user_id}'")
    return JsonResponse({'Mining': 'Done'})


@csrf_exempt
def done_first_login(request):
    """Метка первого захода"""
    # username = request.POST.get('username')
    user_id = request.POST.get('user_id')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE users set first_login = False where ref_code = '{user_id}'")
    return JsonResponse({'first_login': 'Done'})


@csrf_exempt
def switch_region(request):
    """Изменение региона"""
    # username = request.POST.get('username')
    user_id = request.POST.get('user_id')
    region = request.POST.get('region')
    cursor = connection.cursor()
    cursor.execute(f"UPDATE users set region = '{region}' where ref_code = '{user_id}'")
    return JsonResponse({'New region': f'{region}'})


@csrf_exempt
def advertising_see(request):
    """Счет просмотра рекламы"""
    # username = request.POST.get('username')
    user_id = request.POST.get('user_id')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM users where ref_code = '{user_id}'")
    user = cursor.fetchall()
    cursor.execute(f"UPDATE users set tickets = {int(user[0][11])+1}, advertising_limit = {int(user[0][20])-1} where ref_code = '{user_id}'")
    return JsonResponse({'advertising see': 'done'})




