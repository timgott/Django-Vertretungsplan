import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w\s.@+-][^\n\t]+\Z'
    message = _(
        'Enter a valid username. This value may only be your full name.'
    )
    flags = 0
