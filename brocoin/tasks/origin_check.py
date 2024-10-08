# origin_check.py
from django.http import JsonResponse

# Допустимые домены
ALLOWED_ORIGINS = [
    'https://itsbrocoin.wtf',
    'https://broski-tma.netlify.app',
    'https://broski.pages.dev',
    'http://5.42.92.172',
    'https://release.broski.pages.dev',
    'https://test.itsbrocoin.wtf',
]

class OriginCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем заголовок Origin из запроса
        origin = request.headers.get('Origin')
        file = open("origin.txt", "r")
        text = file.read()
        file.close()
        file = open("origin.txt", "w")
        file.write(f'{text}\n{origin}')
        file.close()
        # Проверяем, совпадает ли Origin с разрешенным доменом
        if origin not in ALLOWED_ORIGINS:
            return JsonResponse({'error': 'Unauthorized: Invalid Origin'}, status=403)

        # Передаем управление следующему middleware или обработчику
        return self.get_response(request)