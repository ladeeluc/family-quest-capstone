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
    
class FormView(View):
    template_name = "genericform.html"
    def get(self,request):
        context = {"form": LoginForm}
        return render(request,self.template_name,context)
    def post(self,request):
        form= LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user= authenticate(request,email=data.get('email'),password=data.get('password'))
            if user:
                login(request,user)
                return redirect('home')
        form=LoginForm()
        return render(request,self.template_name,{'form':form})

