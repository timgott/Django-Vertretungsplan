
from .models import Vplan, VplanSchuelerEntry
from .vplan_parser import convertPDF



def fill_blanks(dicts, needed):
    for i in needed:
        if i not in dicts.keys():
            dicts[i] = '-'
    return dicts

def reverse_date(date):
    date = date.split('-')
    day = date[0]
    date[0] = date[2]
    date[2] = day
    return date[0] + '-' + date[1] + '-' + date[2]

def post_row(row, vplan_id, model):
    
    post = model(pos = row['Pos'], fach = row['Fach'], klasse = row['Klasse'], raum = row['Raum'], art = row['Art'], info = row['Info'], vplan = vplan_id )
    post.save()
        
def post_table(file_path, model, needed):
    tables = convertPDF(file_path)
    vplanDate = reverse_date(tables[0].date)
    post = Vplan(vplanDate = vplanDate)
    post.save()
    vplan = Vplan.objects.all().latest('vplanUploadDate')
    vplan_id = vplan

    for table in tables:
        for row in table.rows:
            fill_blanks(row, needed)
            row['Klasse'] = table.title
            post_row(row, vplan_id, model)

def get_query(neu = True, filter = None ):
    if neu == True:
        vplan = Vplan.objects.all().order_by('-vplanUploadDate')[0]
        vplan_date = vplan.vplanDate
    else:
        latest_vplan = Vplan.objects.all().latest('vplanUploadDate')
        vplan = Vplan.objects.exclude(vplanDate__exact = latest_vplan.vplanDate).order_by('-vplanUploadDate')[0]
        vplan_date = vplan.vplanDate
    
    if filter == None:
        query_results = vplan.vplanschuelerentry_set.all()
    else:
        query_results = vplan.vplanschuelerentry_set.filter(klasse__in=('11'))
    
    if query_results.exists():
        lists = []
        last_klasse = query_results[0].klasse
        temp_list = []

        for item in query_results:
            
            if item.klasse == last_klasse:
                temp_list.append(item)
            else:
                lists.append(temp_list)
                temp_list = []
                temp_list.append(item)
                
            last_klasse = item.klasse
        if temp_list not in lists:
            lists.append(temp_list)
        return (lists, vplan_date)
    else:
        return (False, False)
