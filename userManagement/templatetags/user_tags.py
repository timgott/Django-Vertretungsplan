from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter()
def has_group(user, group_name):
    group_name = group_name.split(', ')
    user_groups = user.groups.values_list('name', flat=True)

    for g_n in group_name:
        if g_n in user_groups:
            return True

    return False

