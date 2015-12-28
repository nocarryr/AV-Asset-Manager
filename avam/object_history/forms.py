from django import forms

class ObjectHistoryForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
    def save(self, *args, **kwargs):
        return super(ObjectHistoryForm, self).save(commit=False)
    
def get_object_history_form(object_update):
    model = object_update.content_object._meta.model
    d = object_update.reconstruct()
    form = forms.modelform_factory(model, form=ObjectHistoryForm)
    return form(initial=d['values'])
    
