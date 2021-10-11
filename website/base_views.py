from django.http.response import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
)
from django.views.generic import View
from django.middleware.csrf import get_token

class JsonResponseUpdated(JsonResponse):
    status_code = 201

class BaseEndpoint(View):
    """
    | Method         | Use                  |
    | :------------- | :------------------- | 
    | self.ok        | Send 200/json + CSRF |
    | self.done      | Send 201/json + CSRF |
    | self.not_ok    | Send 400             |
    | self.not_found | Send 404             |
    | self.no_perms  | Send 403             |
    """

    def _csrf(self, request, response: HttpResponse):
        response.headers['X-CSRFToken'] = get_token(request)
        return response

    def ok(self, request, data):
        """Sets `X-CSRFToken` header"""
        return self._csrf(request, JsonResponse(data))
    
    def done(self, request, data):
        """Sets `X-CSRFToken` header"""
        return self._csrf(request, JsonResponseUpdated(data))
    
    def not_ok(self):
        return HttpResponseBadRequest()
    
    def not_found(self):
        return HttpResponseNotFound()
    
    def no_perms(self):
        return HttpResponseForbidden()
    

