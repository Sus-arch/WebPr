import json


class CookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'user_preferences' in request.COOKIES:
            try:
                request.user_preferences = json.loads(request.COOKIES['user_preferences'])
            except:
                request.user_preferences = {}
        else:
            request.user_preferences = {}

        response = self.get_response(request)

        if hasattr(request, 'user_preferences'):
            response.set_cookie('user_preferences', json.dumps(request.user_preferences), max_age=3600 * 24 * 30)

        return response