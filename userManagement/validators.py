import re
import ast

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError

def class_validator(value):
    message = '%(value)s ist keine valide Klasse!'
    code = 'invalid'
    params = {'value': value}
    if type(value) is not str:
        raise ValidationError(message, code, params)
    else:
        if len(value) < 3:
            try:
                if int(value) > 14 or int(value)<5:
                    raise ValidationError(message, code, params)
            except:
                if int(value[0]) < 5:
                    raise ValidationError(message, code, params)
                elif re.search("[a-z]$", value) == None:
                    raise ValidationError(message, code, params)
        else:
            try:
                if int(value[0:2]) <= 10:
                    if re.search("[a-z]$", value) == None:
                        raise ValidationError(message, code, params)
                elif int(value) > 10:
                    raise ValidationError(message, code, params)
            except:
                raise ValidationError(message, code, params)

def kurs_validator(value):
    message = '%(value)s ist kein valider Kurs!'
    code = 'invalid'
    params = {'value': value}
    value = ast.literal_eval(value)
    for val in value:
        if type(val) is not str:
            raise ValidationError(message, code, params)
        else:
            try: 
                if type(int(val[-1])) is int:
                    for i in val[0:-1]:
                        if not (i.isalpha() or i == '/'):
                            raise ValidationError(message, code, params)
            except:
                raise ValidationError(message, code, params)

# must stay for some reason
class UnicodeClassValidator(validators.RegexValidator):
    regex = r'^(\d{2}[a-z])|^\d{2}'
    message = (
        'Bitte die richtige Klasse angeben, nicht den Kurs!'
    )
    flags = 0
