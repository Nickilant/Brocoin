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

        # google_metric_error = self.check_google_metric_id(request)
        # if google_metric_error:
        #     return google_metric_error
        headers = request.headers

        with open("headers.txt", "a") as file:
            file.write(f'{headers}\n')

        #self.log_headers_to_file(request)
        # Получаем заголовок Origin из запроса
        origin = request.headers.get('Origin')
        with open("origin.txt", "a") as file:
            file.write(f'{origin}\n')

        # Проверяем, совпадает ли Origin с разрешенным доменом
        if origin not in ALLOWED_ORIGINS:
            return JsonResponse({'error': 'Unauthorized: Invalid Origin'}, status=403)

        # Передаем управление следующему middleware или обработчику
        return self.get_response(request)

    def log_headers_to_file(self, request):
        request_data = {
            'method': request.method,
            'path': request.path,
            'headers': dict(request.headers),  # Преобразуем заголовки в словарь
        }

        # Логируем данные
        logging.debug(f'Request data: {request_data}')

    def check_google_metric_id(self, request):
        # Проверяем наличие заголовка google_metric_id
        google_metric_id = request.META.get('HTTP_GOOGLE_METRIC_ID')
        if google_metric_id is None:
            return JsonResponse(
                {"error": "Мне кажется что ты чайник"},
                status=418  # Вы можете изменить статус на любой, который вам нужен
            )
        return None
