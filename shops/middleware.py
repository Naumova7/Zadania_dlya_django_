import logging

logger = logging.getLogger("shops")


class APIMethodLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith("/api/"):
            resolver_match = request.resolver_match

            if resolver_match and resolver_match.url_name in {
                "organizations_list",
                "shop_update",
                "organization_shops_file",
            }:
                logger.info(f"API call: {resolver_match.url_name}")

        return response