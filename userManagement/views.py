from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache

from customUser.forms import UserCreationForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account für {username} erstellt! Der Account wird nun von der AG geprüft und dann freigschaltet!')
            return redirect('login')
    else:
        form = UserCreationForm()
    messages.info(request, 'Die Anmeldeberechtigungen werden von der AG geprüft und dann freigeschaltet. Dies kann eine Zeit lang dauern. Die Freischaltung wird dann durch eine Mail bestätigt.')
    context = {'form': form}
    return render(request, 'userManagement/register.html', context)

@never_cache
@login_required
def logout(request):
    auth_logout(request)
    
    messages.success(request, 'Sie wurden erfolgreich abgemeldet!')
    return redirect('login')