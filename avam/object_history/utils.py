import sys
import datetime
import json

from django.utils import timezone

PY2 = sys.version_info.major == 2

def iter_fields(obj, query_lookup=None):
    m = obj._meta
    for f in m.get_fields():
        if query_lookup is None:
            fname = f.name
        else:
            fname = '__'.join([query_lookup, f.name])
        if f.is_relation:
            if f.many_to_many or f.one_to_many:
                for _obj in getattr(obj, f.name).all():
                    yield m, fname, f, _obj.pk
            else:
                yield m, fname, f, getattr(obj, f.name).pk
        else:
            yield m, fname, f, getattr(obj, f.name)
    
def get_query_value(obj, query_lookup):
    if '__' not in query_lookup:
        value = getattr(obj, query_lookup)
        f = obj._meta.get_field(query_lookup)
        if f.is_relation:
            if f.many_to_many or f.one_to_many:
                return [_obj.pk for _obj in value.all()]
            else:
                return value.pk
        else:
            return value
    attr = query_lookup.split('__')[0]
    query_lookup = '__'.join(query_lookup.split('__')[1:])
    return get_query_value(getattr(obj, attr), query_lookup)

PY_TYPES = dict(
    int=int,
    str=str,
    float=float,
    bool=bool,
    NoneType=None,
)

if PY2:
    PY_TYPES['unicode'] = unicode

def str_to_value(s, py_type):
    if 'datetime' in py_type:
        dtcls = py_type.split('.')[1]
        if dtcls == 'datetime':
            dt_fmt = '%Y-%m-%d %H:%M:%S'
            if '.' in s:
                dt_fmt = '.'.join([dt_fmt, '%f'])
            dt_fmt = '+'.join([dt_fmt, '00:00'])
            dt = datetime.datetime.strptime(s, dt_fmt)
            value = timezone.utc.localize(dt)
        elif dtcls == 'time':
            if '.' in s:
                s = ':'.join(s.split('.'))
            args = [int(arg) for arg in s.split(':')]
            value = datetime.time(*args)
        elif dtcls == 'date':
            args = [int(arg) for arg in s.split('-')]
            value = datetime.date(*args)
        elif dtcls == 'timedelta':
            value = datetime.timedelta(float(s))
    elif py_type == 'list':
        return json.loads(s)
    else:
        if py_type == 'bool':
            return {'True':True, 'False':False}.get(s)
        if py_type == 'unicode' and not PY2:
            py_type = 'str'
        py_type = PY_TYPES.get(py_type)
        if py_type is None:
            value = None
        else:
            value = py_type(s)
    return value

def value_to_str(value):
    if isinstance(value, list):
        return json.dumps(value)
    if isinstance(value, datetime.timedelta):
        value = value.total_seconds()
    if PY2:
        return unicode(value)
    return str(value)
