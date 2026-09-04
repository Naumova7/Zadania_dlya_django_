import logging

logger = logging.getLogger("shops")


class APIMethodLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/"):
            logger.info(f"API method: {request.method}")

        response = self.get_response(request)

        return response