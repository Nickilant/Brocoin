# origin_check.py
from django.http import JsonResponse

# Допустимые домены
ALLOWED_ORIGINS = [
    'https://itsbrocoin.wtf',
]

class OriginCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем заголовок Origin из запроса
        origin = request.headers.get('Origin')

        # Проверяем, совпадает ли Origin с разрешенным доменом
        if origin not in ALLOWED_ORIGINS:
            return JsonResponse({'error': 'Unauthorized: Invalid Origin'}, status=403)

        # Передаем управление следующему middleware или обработчику
        return self.get_response(request)