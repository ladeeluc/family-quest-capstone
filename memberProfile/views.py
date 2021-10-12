
from django.shortcuts import render , HttpResponseRedirect,reverse 
from familystructure.models import Person,Relation
from useraccount.models import UserAccount
from django.contrib.auth.decorators import login_required
from memberProfile.forms import AddProfileForm


def member_detail(request, id):
    member= Person.objects.get(id=id)
    return render(request,"profile_detail.html", {'member': member} )


# @login_required # will go to log in page if not logged in 
def add_member(request):
    if request.method == "POST":
        form= AddProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            member: Person = Person.objects.create( 
                first_name = data['first_name'],
                nickname = data['nickname'],    
                middle_name = data['middle_name'],
                last_name = data['last_name'],  
                title = data['title'],
                tagline =data['tagline'],
                birth_date= data['birth_date'],
                death_date  = data['death_date'],
                is_claimed = data['is_claimed'],
                facts = data['facts']          
                )
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('profile_view', args=(id,)))
    form=AddProfileForm()

    return render(request, "generic_form.html", {"form": form})