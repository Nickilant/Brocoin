from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def get_tasks(request):
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
                'links': task[4],
                'complete': complete_task
            })
        return JsonResponse(answer, safe=False)
    else:
        return JsonResponse({'error': 'task not exist'}, safe=False)

