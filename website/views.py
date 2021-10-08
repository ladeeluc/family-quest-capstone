from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth import login, logout, authenticate
from useraccount.forms import LoginForm, SignUpForm
from useraccount.models import UserAccount


# Create your views here.
def homepage_view(request):
    
    return render(request,'index.html')

def signup_view(request):
    if request.method == 'POST': # if the form has been submitted
        form = SignUpForm(request.POST) #get the data
        if form.is_valid():
            UserAccount.objects.create_user( #create_user handles password encryption
                email = form.cleaned_data.get('email'),
                password = form.cleaned_data.get('password'),
                )
            user= authenticate(
                request,email=form.cleaned_data.get('email'),password=form.cleaned_data.get('password'))
            if user:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        form= LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user= authenticate(request,email=data.get('email'),password=data.get('password'))
            if user:
                login(request,user)
                return redirect('home')
    form=LoginForm()
    return render(request,'genericform.html',{'form':form})
