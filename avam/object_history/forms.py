from django import forms

class ObjectHistoryForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        self.updates = kwargs.pop('updates')
        self.changed_fields = kwargs.pop('changed')
        super(ObjectHistoryForm, self).__init__(*args, **kwargs)
    def iter_with_changes(self):
        for name in self.fields:
            yield self[name], name in self.changed_fields
    def save(self, *args, **kwargs):
        return super(ObjectHistoryForm, self).save(commit=False)
    
def get_object_history_form(object_update):
    model = object_update.content_object._meta.model
    d = object_update.reconstruct()
    form = forms.modelform_factory(model, form=ObjectHistoryForm)
    return form(initial=d['values'], updates=d['updates'], changed=d['changed'])
    
