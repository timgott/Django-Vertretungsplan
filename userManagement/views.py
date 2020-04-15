import ast

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect


from customUser.forms import UserCreationForm

from .forms import UserUpdateForm, SchuelerProfileUpdateForm, LehrerProfileUpdateForm
from .models import SchuelerProfile
from .functions import create_dict, get_profile_form
from .decorators import has_profile

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            SchuelerProfile.objects.create(user=user)
            group = Group.objects.get(name='schueler')
            user.groups.add(group)

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

@has_profile(redirect_url = 'logout')
@csrf_protect
@login_required
def profile(request):
    active_tab = 'username-mail'

    if request.method == 'POST':

        if 'u_form' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if u_form.is_valid():
                u_form.save()
            p_c_form = PasswordChangeForm(request.user)
            p_form, kurse_list = get_profile_form(request.user)
            active_tab = 'username-mail'

        elif 'p_form' in request.POST:

            p_form, kurse_list = get_profile_form(request.user, request.POST)
            if p_form.is_valid():
                p_form.save()
            p_c_form = PasswordChangeForm(request.user)
            u_form = UserUpdateForm(instance=request.user)
            active_tab = 'change-class'

        elif 'p_c_form' in request.POST:
            p_c_form = PasswordChangeForm(request.user, request.POST)
            if p_c_form.is_valid():
                user = p_c_form.save()
                # Updating the password logs out all other sessions for the user
                # except the current one.
                update_session_auth_hash(request, user)
                messages.success(request, 'Ihr Passwort wurde erfolgreich geändert')

            else:
                active_tab = 'change-password'
            p_form, kurse_list = get_profile_form(request.user)
            u_form = UserUpdateForm(instance=request.user)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form, kurse_list = get_profile_form(request.user)
        p_c_form = PasswordChangeForm(request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'p_c_form': p_c_form,
        'active_tab': active_tab,
        'kurse_list': kurse_list,
    }

    return render(request, 'userManagement/profile.html', context)