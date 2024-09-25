from django.http import JsonResponse

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for a custom header to restrict access
        if request.headers.get('X-Restricted-Access') == 'true':
            return JsonResponse({'error': 'Access restricted'}, status=403)

        response = self.get_response(request)
        return response