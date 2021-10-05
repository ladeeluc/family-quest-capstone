from django.http import JsonResponse
from django.views.generic import View

class BaseEndpoint(View):
    """
    Example:

    def get(request):
        return JsonResponse({
            'data': list(Model.objects.values())
        })
    """
    

