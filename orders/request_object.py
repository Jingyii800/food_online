from . import models

def request_object_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        models.request_object = request

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware