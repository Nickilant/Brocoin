# origin_check.py
from django.http import JsonResponse
import logging
import os

logger = logging.getLogger(__name__)

# Допустимые домены
ALLOWED_ORIGINS = [
    'https://itsbrocoin.wtf',
    'https://broski-tma.netlify.app',
    'https://broski.pages.dev',
    'http://5.42.92.172',
    'https://release.broski.pages.dev',
    'https://test.itsbrocoin.wtf',
]
logging.basicConfig(filename='request_log.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')


class OriginCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        google_metric_error = self.check_google_metric_id(request)
        if google_metric_error:
            return google_metric_error
        headers = request.headers.get('Google-Metric-Id')
        data = request.POST.get('user_id')

        with open("headers.txt", "a") as file:
            file.write(f'{headers} body: {data}\n')

        # Получаем заголовок Origin из запроса
        origin = request.headers.get('Origin')
        with open("origin.txt", "a") as file:
            file.write(f'{origin}\n')

        # Проверяем, совпадает ли Origin с разрешенным доменом
        if origin not in ALLOWED_ORIGINS:
            return JsonResponse({'error': 'Unauthorized: Invalid Origin'}, status=403)

        # Передаем управление следующему middleware или обработчику
        return self.get_response(request)

    def check_google_metric_id(self, request):
        # Проверяем наличие заголовка google_metric_id
        google_metric_id = request.headers.get('Google-Metric-Id')
        if google_metric_id is None:
            if self.decode(encoded_key=google_metric_id, shift=3, request=request):
                return None
            else:
                return JsonResponse(
                    {"error": "Мне кажется что ты чайник"},
                    status=418  # Вы можете изменить статус на любой, который вам нужен
                )
        return None

    def decode(self, encoded_key, shift, request):
        trimmed_key = encoded_key[3:-3]  # Убираем случайные символы
        decoded = ''.join(chr(ord(char) - shift) for char in trimmed_key)
        if decoded.split('_')[0] == request.POST.get('user_id'):
            return True
        else:
            return False
