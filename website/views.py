from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth import login, logout, authenticate
from useraccount.forms import LoginForm
from useraccount.models import UserAccount


# Create your views here.
def homepage_view(request):
    
    return render(request,'index.html',{'form':form})

def signup_view(request):
    if request.method == 'POST': # if the form has been submitted
        form = LoginForm(request.POST) #get the data
        if form.is_valid():
            UserAccount.objects.create_user( #create_user handles password encryption
                username = form.cleaned_data.get('username'),
                password = form.cleaned_data.get('password'),
                )
            user= authenticate(
                request,username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password'))
            if user:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            
    else:
        form = LoginForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
