import datetime

from django.core.exceptions import ValidationError
from django import forms

class HoursField(forms.DurationField):
    def __init__(self, **kwargs):
        kwargs['label_suffix'] = ' (Hours)'
        super(HoursField, self).__init__(**kwargs)
    def prepare_value(self, value):
        if isinstance(value, datetime.timedelta):
            s = value.total_seconds()
            return str(s / 3600)
        return value
    def to_python(self, value):
        if value in self.empty_values:
            return None
        if isinstance(value, datetime.timedelta):
            return value
        if isinstance(value, basestring):
            if '.' in value:
                if value.count('.') > 2:
                    value = None
                elif False in [v.isdigit() for v in value.split('.')]:
                    value = None
                value = float(value)
            elif not value.isdigit():
                value = None
            else:
                value = int(value)
        if value is None:
            raise ValidationError(self.error_messages['invalid'], code='invalid')
        return datetime.timedelta(hours=value)
