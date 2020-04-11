from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import SchuelerProfile, LehrerProfile

def allowed_users(allowed_roles=[], redirect_url=None):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            allowed_roles.append('admin')
            groups = None
            if request.user.groups.exists():
                groups = request.user.groups.all()
            
            if groups is None:
                if redirect_url != None:
                    return redirect(redirect_url)
                
                else:
                    return HttpResponse('You are not allowed to view this page!')

            for g in groups:
                if g.name in allowed_roles:
                    return view_func(request, *args, **kwargs)
                
                elif redirect_url != None:
                    return redirect(redirect_url)
                
                else:
                    return HttpResponse('You are not allowed to view this page!')
        return wrapper_func
    return decorator

def has_profile(redirect_url=None):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            schuelerprofile_check = SchuelerProfile.objects.all()
            lehrerprofile_check = LehrerProfile.objects.all()
            if schuelerprofile_check.filter(user=request.user).exists() or lehrerprofile_check.filter(user=request.user).exists():
                return view_func(request, *args, **kwargs)

            elif redirect_url != None:
                messages.error(request, 'Du hast kein Profil. Bitte kontaktiere einen Admin!')
                return redirect(redirect_url)

            else: 
                return HttpResponse('Du hast kein Profil. Bitte kontaktiere einen Admin!')

        return wrapper_func
    return decorator
