from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.mixins import LoginRequiredMixin

from object_history.models import ObjectUpdate
from object_history.forms import get_object_history_form

class ObjectUpdateMixin(object):
    def get_object_history_queryset(self, object_update=None):
        if object_update is not None:
            object_update = self.object_update
        q = object_update.get_update_queryset()
        return q

class SingleObjectUpdateMixin(SingleObjectMixin, ObjectUpdateMixin):
    """
    Retrieves a single object and its update history
    """
    def get_object(self, queryset=None):
        """
        Returns the object to get update history from
        
        If the `model` class attribute is defined and the object can be
        retrieved with the `SingleObjectMixin` method, that will be used.
        
        Alternatively, the url conf can be used to supply the following:
            content_type: The content_type id for the object model
            object_id: The object's primary key
        
        If no `model` is defined and the above url kwargs are not present,
        the lookup will be performed using `ObjectUpdate` as the model and
        the instance referenced will be used to return the object that it
        is tracking.
        """
        self.object_update = None
        if self.model is not None:
            return super(SingleObjectUpdateMixin, self).get_object(queryset)
        ctype_pk = self.kwargs.get('content_type')
        obj_id = self.kwargs.get('object_id')
        if ctype_pk is None and obj_id is None:
            obj_update = super(SingleObjectUpdateMixin, self).get_object(queryset)
            self.object_update = obj_update
            return obj_update.content_object
        content_type = ContentType.objects.get(pk=ctype_pk)
        m = content_type.model_class()
        queryset = m.objects.all()
        try:
            obj = queryset.get(pk=obj_id)
        except m.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name':m._meta.verbose_name})
        return obj
    def get_queryset(self):
        if self.model is None:
            return ObjectUpdate.objects.all()
        return super(SingleObjectUpdateMixin, self).get_queryset()
    def get_context_data(self, **kwargs):
        context = super(SingleObjectUpdateMixin, self).get_context_data(**kwargs)
        if self.object_update is not None:
            context['object_update'] = self.object_update
            q = self.get_object_history_queryset(self.object_update)
            context['object_history_queryset'] = q
        else:
            obj = context['object']
            q = ObjectUpdate.objects.get_for_object(obj)
            context['object_history_queryset'] = q
            context['object_update'] = self.object_update = q.latest('datetime')
        return context

class BaseObjectHistoryView(LoginRequiredMixin, SingleObjectUpdateMixin, View):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class ObjectHistory(SingleObjectTemplateResponseMixin, BaseObjectHistoryView):
    template_name = 'object_history/object_history.html'
    def get_context_data(self, **kwargs):
        context = super(ObjectHistory, self).get_context_data(**kwargs)
        context['object_form'] = get_object_history_form(self.object_update)
        return context
    
