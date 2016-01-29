from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.views.generic import ListView

from assets.models import AssetBase

def get_model_map():
    a_by_name = {m._meta.model_name:m for m in AssetBase.iter_subclasses()}
    ct_by_name = ContentType.objects.get_for_models(*a_by_name.values())
    d = {'by_name':{}, 'by_id':{}}
    for name, m in a_by_name.items():
        ct = ct_by_name[name]
        _d = dict(
            content_type=ct,
            id=ct.id,
            model_name=name,
            model=m,
        )
        d['by_name'][name] = _d
        d['by_id'][ct.id] = _d
    d['all_ids'] = d['by_id'].keys()[:]
    return d

model_map = get_model_map()

class ContentTypeQuerySet(QuerySet):
    pass

def content_types_queryset():
    m = ContentType.objects
    q = ContentTypeQuerySet(model=ContentType, using=m._db, hints=m._hints)
    return q.filter(id__in=model_map['all_ids'])

class AssetList(ListView):
    pass
