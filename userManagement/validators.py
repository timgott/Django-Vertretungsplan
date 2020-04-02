import re

from django.core import validators
from django.utils.deconstruct import deconstructible

class UnicodeClassValidator(validators.RegexValidator):
    regex = r'^(\d{2}[a-z])|^\d{2}'
    message = (
        'Bitte die richtige Klasse angeben, nicht den Kurs!'
    )
    flags = 0