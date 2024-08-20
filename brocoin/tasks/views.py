from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_tasks(request):
    """Получение данных по таскам"""
    cursor = connection.cursor()
    username = request.POST.get('username')
    cursor.execute(f"SELECT * FROM tasks")
    tasks = cursor.fetchall()
    if tasks:
        answer = []
        for task in tasks:
            cursor.execute(f"SELECT sid from users where username = '{username}'")
            user_sid = cursor.fetchall()
            cursor.execute(f"SELECT * FROM user_tasks where user_id = '{user_sid[0][0]}' AND task_id = {task[0]}")
            complete = cursor.fetchall()
            if complete:
                complete_task = True
            else:
                complete_task = False
            answer.append({
                'id': task[0],
                'description': task[1],
                'points': task[2],
                'tickets': task[5],
                'duration': task[6],
                'links': task[4],
                'complete': complete_task
            })
        return JsonResponse({'tasks': answer}, safe=False)
    else:
        return JsonResponse({'error': 'task not exist'}, safe=False)


@csrf_exempt
def done_tasks(request):
    """Выполнение таски"""
    cursor = connection.cursor()
    username = request.POST.get('username')
    task_id = request.POST.get('task_id')
    cursor.execute(f"SELECT sid from users where username = '{username}'")
    user_sid = cursor.fetchall()
    cursor.execute(f"INSERT INTO public.user_tasks (user_id, task_id) VALUES ('{user_sid[0][0]}', '{int(task_id)}')")
    return JsonResponse({'tasks_done': 'complete'})
