from django.shortcuts import redirect
from django.http import HttpResponse

def allowed_users(allowed_roles=[], redirect_url=None):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            groups = None
            if request.user.groups.exists():
                groups = request.user.groups.all()
            
            for g in groups:
                if g.name in allowed_roles:
                    return view_func(request, *args, **kwargs)
                
                elif redirect_url != None:
                    return redirect(redirect_url)
                
                else:
                    return HttpResponse('You are not allowed to view this page!')
        return wrapper_func
    return decorator
