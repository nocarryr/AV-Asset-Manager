from django.http import JsonResponse
from django.views.generic import ListView
from django.db.models import Q

from categories.models import Category, CategoryItem

def get_qdict(request):
    if request.method == 'POST':
        d = request.POST
    elif request.method == 'GET':
        d = request.GET
    else:
        d = None
    return d

def get_content_objects_from_query(qdict, queryset):
    obj_data_list = qdict.getlist('content_object')
    if not obj_data_list:
        return queryset.none()
    qexp = None
    for obj_data in obj_data_list:
        content_type_id, obj_id = obj_data.split('-')
        qkwargs = dict(object_id=obj_id, content_type__id=content_type_id)
        if qexp is None:
            qexp = Q(**qkwargs)
        else:
            qexp = qexp | Q(**qkwargs)
    return queryset.filter(qexp)

class JsonResponseMixin(object):
    def render_to_json_response(self, context, **kwargs):
        data = context.get('data', self.get_data(context))
        return JsonResponse(data, **kwargs)
    def get_data(self, context):
        return {}

class CategoriesForObjects(ListView, JsonResponseMixin):
    model = CategoryItem
    context_object_name = 'category_items'
    template_name = 'categories/category-list.html'
    def get_queryset(self):
        q = super(CategoriesForObjects, self).get_queryset()
        qdict = get_qdict(self.request)
        if qdict is None:
            return q.none()
        return get_content_objects_from_query(qdict, q)
    def get_categories(self, context):
        citems = context['category_items']
        vl = citems.values_list('category', flat=True)
        return Category.objects.filter(id__in=vl)
    def get_data(self, context):
        d = {'by_object':{}, 'by_category':{}}
        for citem in context['category_items']:
            obj_key = '{0}-{1}'.format(citem.content_type.pk, citem.object_id)
            cat_key = str(citem.category)
            if obj_key not in d['by_object']:
                d['by_object'][obj_key] = {}
            if cat_key not in d['by_category']:
                d['by_category'][cat_key] = {}
            obj_data = {
                'content_object_key':obj_key,
                'category_item__id':citem.id,
                'category__name':citem.category.name,
                'category__id':citem.category.id,
                'category_key':cat_key,
            }
            d['by_object'][obj_key][str(citem.category)] = obj_data
            d['by_category'][cat_key] = obj_data
        return d
    def get_context_data(self, **kwargs):
        context = super(CategoriesForObjects, self).get_context_data(**kwargs)
        context['categories'] = self.get_categories(context)
        return context
    def render_to_response(self, context, **kwargs):
        if kwargs.get('json') or self.kwargs.get('json'):
            return self.render_to_json_response(context, **kwargs)
        return super(CategoriesForObjects, self).render_to_response(context, **kwargs)
