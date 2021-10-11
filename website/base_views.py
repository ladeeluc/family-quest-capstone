from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import HttpResponse, render, redirect
from useraccount.forms import LoginForm
from django.contrib.auth import login, logout, authenticate

class BaseEndpoint(View):
    """
    Example:

    def get(request):
        return JsonResponse({
            'data': list(Model.objects.values())
        })
    """
    
class GenericFormView(View):
    """
    Override NotImplemented methods and functions with appropriate data.
    Handles serving empty forms and validating posted forms.
    _handle_submission() will be called after validation.
    _handle_submission() can return a response like normal to redirect the user
    or serve alternate post-submission content.
    """
    FormClass = NotImplemented
    template_name = "generic_form.html"
    template_text = {"header":"Generic Form", "submit":"Submit"}

    def get(self, request, *args, **kwargs):
        form = self.FormClass()
        return render(request, self.template_name, {"form": form, "template_text": self.template_text})

    def post(self, request, *args, **kwargs):
        form = self.FormClass(request.POST)
        if form.is_valid():
            res = self._handle_submission(request, form.cleaned_data)
            if res:
                return res
        return render(request, self.template_name, {"form": form, "template_text": self.template_text})

    def _handle_submission(self, request, form):
        return NotImplemented

