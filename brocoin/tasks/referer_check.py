# referer_check.py
from django.http import JsonResponse

# Допустимые URL (рефереры)
ALLOWED_REFERERS = [
    'https://itsbrocoin.wtf/',
    'https://broski-tma.netlify.app/',
]

class RefererCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        referer = request.headers.get('Referer')

        if not referer or not any(referer.startswith(allowed) for allowed in ALLOWED_REFERERS):
            return JsonResponse({'error': 'Unauthorized: Invalid Referer'}, status=403)

        return self.get_response(request)