def create_dict(queryset):
    querydict = dict(queryset)
    querydict['klasse'] = querydict['klasse'][0]
    while '' in querydict['kurse']:
        querydict['kurse'].remove('')
    return querydict