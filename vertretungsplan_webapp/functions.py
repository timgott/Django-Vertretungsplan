import ast

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

def remove_not_needed(dict, needed):
    keys = list(dict.keys())
    for key in keys:
        if key not in needed:
            dict.pop(key)

def post_row(row, vplan_id, model):
    row = {k[0].lower()+k[1:]: v for k, v in row.items()}

    post = model(vplan = vplan_id, **row )
    post.save()

def post_table(file_path, model, needed, vplan_type):
    tables = convertPDF(file_path)
    vplanDate = reverse_date(tables[0].date)
    post = Vplan(vplanDate = vplanDate, vplanType = vplan_type)
    post.save()

    vplan = Vplan.objects.all().latest('vplanUploadDate')
    vplan_id = vplan

    for table in tables:
        for row in table.rows:
            last_row_index = table.rows.index(row) - 1
            last_row = table.rows[last_row_index]

            fill_blanks(row, last_row, needed)

            if vplan_type == 'schueler':
                row['Klasse'] = table.title
            elif vplan_type == 'lehrer':
                row['Lehrer'] = row.pop('Lehrer Name')
                row['LehrerName'] = table.title

            remove_not_needed(row, needed)

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

def get_query(vplan_type, filter=None, neu = True):
    latest = Vplan.objects.all().filter(vplanType__exact = vplan_type).latest('vplanDate','vplanUploadDate')
    
    if neu == True:
        vplan = latest
        vplan_date = vplan.vplanDate
    else:
        vplan = Vplan.objects.exclude(vplanDate__exact = latest.vplanDate).filter(vplanType__exact = vplan_type).order_by('-vplanDate','-vplanUploadDate')[0]
        vplan_date = vplan.vplanDate

    if vplan_type == 'schueler':
        qs = vplan.schueler
    elif vplan_type == 'lehrer':
        qs = vplan.lehrer

    if filter == None:
        query_results = qs.all()
        lists = query_to_list(query_results)
        return (lists, vplan_date, None)
    else:
        query_filtered = qs.filter(**filter)
        query_rest = qs.exclude(**filter)

        list_filtered = query_to_list(query_filtered)
        list_rest = query_to_list(query_rest)
        return (list_rest, vplan_date, list_filtered)

def create_dict(keys, values):
    dict = {}
    for key in keys:
        index = keys.index(key)
        if values[index] != [] and values[index] != ['']:
            dict[key] = values[index]
    dict = get_filter(dict)
    return dict

def get_vplan(user):
    kurs_filter = []
    kuerzel_filter = []
    group_names = []
    if user.groups.exists():
        groups = user.groups.all()
        for group in groups:
            group_names.append(group.name)

    if 'schueler' in group_names:
        filter_klasse = [user.schuelerprofile.klasse]

        if user.schuelerprofile.kurse != '':
            kurs_filter = ast.literal_eval(user.schuelerprofile.kurse)

        filter_dict = create_dict(['klasse', 'fach'], [filter_klasse, kurs_filter])
    elif 'lehrer' in group_names:
        kuerzel_filter = [user.lehrerprofile.kuerzel]
        filter_dict = create_dict(['kuerzel'], [kuerzel_filter])
        filter_klasse = []
    else:
        return (None, None, None, None, None, None, None, None, None, None)

    vplan_filtered = []
    vplan_l, vplan_l_date, vplan_l_filtered = (None, None, None)

    if filter_klasse != [] and filter_klasse != ['']:
        vplan, vplan_date, vplan_filtered = get_query(vplan_type = 'schueler', filter=filter_dict, neu = True)
        vplan_a, vplan_a_date, vplan_a_filtered = get_query(vplan_type = 'schueler', filter=filter_dict, neu = False)

    else:
        vplan, vplan_date, vplan_filtered = get_query(vplan_type = 'schueler', neu = True)
        vplan_a, vplan_a_date, vplan_a_filtered = get_query(vplan_type = 'schueler', neu = False)
    if 'lehrer' in group_names or 'admin' in group_names:
        if kuerzel_filter != [] and kuerzel_filter != ['']:
            vplan_l, vplan_l_date, vplan_l_filtered = get_query(vplan_type = 'lehrer', filter = filter_dict , neu = True)
        else:
            vplan_l, vplan_l_date, vplan_l_filtered = get_query(vplan_type = 'lehrer' , neu = True)

    return (vplan, vplan_date, vplan_filtered,
        vplan_a, vplan_a_date, vplan_a_filtered,
        vplan_l, vplan_l_date, vplan_l_filtered,
        kurs_filter
        )

