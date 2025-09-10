import base64
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

class BasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.path.startswith('/static/') or
            request.path.startswith('/media/') or
            request.path in ['/accounts/login/', '/accounts/register/']):
            return self.get_response(request)

        if not request.user.is_authenticated and 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2 and auth[0].lower() == "basic":
                try:
                    username, password = base64.b64decode(auth[1]).decode('utf-8').split(':', 1)
                    user = authenticate(username=username, password=password)
                    if user is not None and user.is_active:
                        login(request, user)
                        request.user = user
                except Exception as e:
                    print(f"Basic Auth error: {e}")
                    pass

        return self.get_response(request)