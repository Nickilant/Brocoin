from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests


@csrf_exempt
def get_tasks(request):
    """Получение данных по таскам"""
    cursor = connection.cursor()
    # username = request.POST.get('username')
    user_id = request.POST.get('user_id')
    cursor.execute(f"SELECT * FROM tasks")
    tasks = cursor.fetchall()
    if tasks:
        answer = []
        for task in tasks:
            cursor.execute(f"SELECT sid from users where ref_code = '{user_id}'")
            user_sid = cursor.fetchall()
            cursor.execute(f"SELECT * FROM user_tasks where user_id = '{user_sid[0][0]}' AND task_id = {task[0]}")
            complete = cursor.fetchall()
            if complete:
                complete_task = True
            else:
                complete_task = False
            answer.append({
                'id': task[0],
                'title': task[1],
                'points': task[2],
                'tickets': task[5],
                'duration': task[6],
                'links': task[4],
                'complete': complete_task,
                'description': task[7],
                'image': task[3],
                'priority': task[9],
                'region': task[10],
            })
        return JsonResponse({'tasks': answer}, safe=False)
    else:
        return JsonResponse({'error': 'task not exist'}, safe=False)


@csrf_exempt
def done_tasks(request):
    """Выполнение таски"""
    cursor = connection.cursor()
    # username = request.POST.get('username')
    user_id = request.POST.get('user_id')
    task_id = request.POST.get('task_id')
    cursor.execute(f"SELECT sid, score, tickets from users where ref_code = '{user_id}'")
    user_sid = cursor.fetchall()
    score = user_sid[0][1]
    tickets = user_sid[0][2]
    cursor.execute(f"INSERT INTO public.user_tasks (user_id, task_id) VALUES ('{user_sid[0][0]}', '{int(task_id)}')")
    cursor.execute(f"SELECT points, tickets from tasks where id = {task_id}")
    taska = cursor.fetchall()
    taska_points = taska[0][0]
    taska_tickets = taska[0][1]
    itog_score = int(score) + int(taska_points)
    try:
        itog_tickets = int(tickets) + int(taska_tickets)
    except Exception as e:
        itog_tickets = int(tickets)
    cursor.execute(f"UPDATE public.users set score = {itog_score}, tickets = {itog_tickets} where ref_code = '{user_id}'")
    return JsonResponse({'tasks_done': 'complete'})

@csrf_exempt
def check_tasks(request):
    """Проверка таски"""
    cursor = connection.cursor()
    # username = request.POST.get('username')
    #TODO возможно понадобится и юзернейм хз
    user_id = request.POST.get('user_id')
    task_id = request.POST.get('task_id')
    cursor.execute(f"SELECT points, tickets from tasks where id = {task_id}")
    taska = cursor.fetchall()
    api = taska[0][8]
    #TODO узнать параметры
    r = requests.post(api, data={'user_id': f'{user_id}'})
    #TODO узнать ответ и в зависимости от него возвращать его на фронт



    return JsonResponse({'task': 'completed'})


