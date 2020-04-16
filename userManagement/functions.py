import ast

from .models import LehrerProfile, SchuelerProfile
from .forms import LehrerProfileUpdateForm, SchuelerProfileUpdateForm

def create_dict(queryset):
    querydict = dict(queryset)
    querydict['klasse'] = querydict['klasse'][0]
    while '' in querydict['kurse']:
        querydict['kurse'].remove('')
    return querydict

def get_profile_form(user, data = None):
    schueler_check = SchuelerProfile.objects.all()
    lehrer_check = LehrerProfile.objects.all()

    if schueler_check.filter(user=user).exists():
        if user.schuelerprofile.kurse != '':
            kurse_list = ast.literal_eval(user.schuelerprofile.kurse)
        else:
            kurse_list = None
        post_dict = create_dict(data)
        return (SchuelerProfileUpdateForm(post_dict, instance = user.schuelerprofile), kurse_list)

    elif lehrer_check.filter(user=user).exists():
        return (LehrerProfileUpdateForm(data, instance = user.lehrerprofile), None)