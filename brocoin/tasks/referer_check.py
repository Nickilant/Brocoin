# referer_check.py
from django.http import JsonResponse

# Допустимые URL (рефереры)
ALLOWED_REFERER = 'https://itsbrocoin.wtf/'

class RefererCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем заголовок Referer из запроса
        referer = request.headers.get('Referer')

        # Проверяем, что реферер начинается с допустимого URL
        if not referer or not referer.startswith(ALLOWED_REFERER):
            return JsonResponse({'error': 'Unauthorized: Invalid Referer'}, status=403)

        # Передаем управление следующему middleware или обработчику
        return self.get_response(request)