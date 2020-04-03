
from .models import Vplan, VplanSchuelerEntry
from .vplan_parser import convertPDF



def fill_blanks(dicts, last_row, needed):
    for i in needed:
        if i not in dicts.keys():
            if 'Pos' in needed and i == 'Pos':
                dicts[i] = last_row[i]
            else:    
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
            last_row_index = table.rows.index(row) - 1
            last_row = table.rows[last_row_index]
            fill_blanks(row, last_row, needed)
            row['Klasse'] = table.title
            post_row(row, vplan_id, model)

def query_to_list(query):
    if query.exists():
        lists = []
        last_klasse = query[0].klasse
        temp_list = []

        for item in query:
            
            if item.klasse == last_klasse:
                temp_list.append(item)
            else:
                lists.append(temp_list)
                temp_list = []
                temp_list.append(item)
                
            last_klasse = item.klasse
        if temp_list not in lists:
            lists.append(temp_list)
        return lists
    else:
        return None

def get_filter(filter_dict):
    keys = list(filter_dict.keys())
    for key in keys:
        new_key = key + '__' + 'in'
        filter_dict[new_key] = filter_dict.pop(key)
    return filter_dict

def get_query(filter, neu = True):
    if neu == True:
        vplan = Vplan.objects.all().order_by('-vplanUploadDate')[0]
        vplan_date = vplan.vplanDate
    else:
        latest_vplan = Vplan.objects.all().latest('vplanUploadDate')
        vplan = Vplan.objects.exclude(vplanDate__exact = latest_vplan.vplanDate).order_by('-vplanUploadDate')[0]
        vplan_date = vplan.vplanDate
    
    if filter == None:
        query_results = vplan.vplanschuelerentry_set.all()
        lists = query_to_list(query_results)
        return (lists, vplan_date, None)
    else:
        query_filtered = vplan.vplanschuelerentry_set.filter(**filter)
        query_rest = vplan.vplanschuelerentry_set.exclude(**filter)

        list_filtered = query_to_list(query_filtered)
        list_rest = query_to_list(query_rest)
        return (list_rest, vplan_date, list_filtered)