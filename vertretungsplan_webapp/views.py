from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from userManagement.decorators import allowed_users

from .forms import VplanUpdateForm


@allowed_users(allowed_roles=['admin', 'uploader'], redirect_url='vplan-home')
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = VplanUpdateForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            print(files)
            for f in files:
                print(f)
                uploaded_file = f
                file_name = uploaded_file.name
                # file_path = f'media/{file_name}'
                fs = FileSystemStorage()
                if fs.exists(file_name):
                    fs.delete(file_name)
                
                fs.save(uploaded_file.name, uploaded_file)
            return redirect('vplan-home')
    else:
        form = VplanUpdateForm()
    return render(request, 'vertretungsplan_webapp/vplan_upload.html', {'form': form})

@login_required
def home(request):
    current_user_groups = request.user.groups.values_list("name", flat=True)
    context = {
        "is_teacher": ("lehrer" in current_user_groups or "admin" in current_user_groups),
        "is_student": "schueler" in current_user_groups,
    }
    return render(request, 'vertretungsplan_webapp/home.html', context)