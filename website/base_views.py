from django.http.response import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
)
from django.views.generic import View

class HttpResponseResourceCreated(HttpResponse):
    status_code = 201

class BaseEndpoint(View):
    """
    | Method         | Use           |
    | :------------- | :------------ | 
    | self.ok        | Send 200/json |
    | self.not_ok    | Send 400      |
    | self.not_found | Send 404      |
    | self.no_perms  | Send 403      |
    """

    def ok(self, data):
        return JsonResponse(data)
    
    def done(self):
        return HttpResponseResourceCreated()
    
    def not_ok(self):
        return HttpResponseBadRequest()
    
    def not_found(self):
        return HttpResponseNotFound()
    
    def no_perms(self):
        return HttpResponseForbidden()
    

