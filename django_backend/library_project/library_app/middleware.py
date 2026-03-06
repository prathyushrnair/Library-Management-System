from library_app.models import AppLog


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Skip admin/static/media noise and only track application traffic.
        if request.path.startswith('/admin/') or request.path.startswith('/static/') or request.path.startswith('/Media/'):
            return response

        user = None
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user

        try:
            AppLog.objects.create(
                user=user,
                level='ERROR' if response.status_code >= 500 else 'WARNING' if response.status_code >= 400 else 'INFO',
                event='REQUEST',
                message=f'{request.method} {request.path}',
                path=request.path,
                method=request.method,
                status_code=response.status_code,
            )
        except Exception:
            # Logging should never break user requests.
            pass

        return response
