from .models import RequestTracking


class RequestTackerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.track_request(request)

        return response

    def track_request(self, request):
        """
        Now, for simplicity tracking ach request after the view is called.
        """
        user = request.user
        if not user.is_anonymous and not user.is_superuser:
            RequestTracking.objects.create(
                user=request.user,
            )
