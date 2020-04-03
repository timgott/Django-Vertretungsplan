import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w\s.@+-][^\n\t]+\Z'
    message = _(
        'Benutzername kann nicht vergeben werden. Bitte gebe deinen vollen Namen ein!'
    )
    flags = 0
