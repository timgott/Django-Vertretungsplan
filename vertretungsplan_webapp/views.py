from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone

from userManagement.decorators import allowed_users

from .forms import VplanUpdateForm
from .models import Vplan, VplanSchuelerEntry

from .functions import get_query, post_table, get_filter, create_dict
from .vplan_parser import convertPDF

@allowed_users(allowed_roles=['uploader'], redirect_url='vplan-home')
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = VplanUpdateForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        if form.is_valid():

            for f in files:

                uploaded_file = f
                file_name = uploaded_file.name
                fs = FileSystemStorage()
                
                if fs.exists(file_name):
                    fs.delete(file_name)
                fs.save(uploaded_file.name, uploaded_file)

                file_path = f'media/{file_name}'
                if 'vplan'in file_name.strip('.pdf') and '.pdf' in file_name.strip('vplan'):
                    needed = ['Pos','Fach','Klasse','Raum','Art','Info']
                    post_table(file_path, VplanSchuelerEntry, needed)
                
            messages.success(request, 'Die Dateien wurden erfolgreich hochgeladen!')
    else:
        form = VplanUpdateForm()
    return render(request, 'vertretungsplan_webapp/vplan_upload.html', {'form': form})

@login_required
def home(request):
    filter_klasse = [request.user.schuelerprofile.klasse]
    kurs_filter = [request.user.schuelerprofile.kurse]
    filter_dict = create_dict(['klasse', 'fach'], [filter_klasse, kurs_filter])
    vplan_filtered = []
    if filter_klasse != []:
        vplan, vplan_date, vplan_filtered = get_query(filter=filter_dict, neu = True)
        vplan_a, vplan_a_date, vplan_a_filtered = get_query(filter=filter_dict, neu = False)

    else:
        vplan, vplan_date, vplan_filtered = get_query(neu = True)
        vplan_a, vplan_a_date, vplan_a_filtered = get_query(neu = False)

    context = {
        'vplan': vplan,
        'vplan_filtered': vplan_filtered,
        'vplan_date': vplan_date,
        'vplan_a': vplan_a,
        'vplan_a_filtered': vplan_a_filtered,
        'vplan_a_date': vplan_a_date,
        'kurs_filter': kurs_filter,
    }
    return render(request, 'vertretungsplan_webapp/home.html', context)