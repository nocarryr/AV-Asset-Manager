from django import forms
from django.utils.safestring import mark_safe

from assettags.models import (
    AssetTagImageTemplate,
    AssetTagPrintTemplate
)

class MDLWidgetMixin(object):
    widget_template = '''
    <div class="%(div_classes)s">
        %(inner_widget)s
        <label class="mdl-selectfield__label" for="%(id)s">%(label)s</label>
    </div>
    '''
    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(MDLWidgetMixin, self).build_attrs(extra_attrs, **kwargs)
        attrs['class'] = self.div_classes
        return attrs
    def render_mdl(self, name, attrs, inner_widget):
        return self.widget_template % dict(
            id=attrs['id'],
            div_classes=self.div_classes,
            inner_widget=inner_widget,
            label=name,
        )

class MDLInputMixin(MDLWidgetMixin):
    div_classes = 'mdl-textfield mdl-js-textfield mdl-textfield--floating-label'
    inner_classes = 'mdl-textfield__input'
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        inner_widget = super(MDLInputMixin, self).render(name, value, final_attrs)
        return mark_safe(self.render_mdl(name, final_attrs, inner_widget))

class MDLTextInput(MDLInputMixin, forms.TextInput):
    pass

class MDLNumberInput(MDLInputMixin, forms.NumberInput):
    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(MDLNumberInput, self).build_attrs(extra_attrs, **kwargs)
        attrs['pattern'] = '-?[0-9]*(\.[0-9]+)?'
        return attrs

class MDLCheckBox(MDLInputMixin, forms.CheckboxInput):
    widget_template = '''
    <label class="%(div_classes)s" for="%(id)s">
        %(inner_widget)s
        <span class="mdl-checkbox__label">%(label)s</span>
    </label>
    '''
    div_classes = 'mdl-checkbox'
    inner_classes = 'mdl-checkbox__input'

class MDLSelect(MDLWidgetMixin, forms.Select):
    div_classes = 'mdl-selectfield mdl-js-selectfield mdl-selectfield--floating-label'
    inner_classes = 'mdl-selectfield__select'
    def render(self, name, value, attrs=None, choices=()):
        final_attrs = self.build_attrs(attrs)
        inner_widget = super(MDLSelect, self).render(name, value, final_attrs, choices)
        return mark_safe(self.render_mdl(name, final_attrs, inner_widget))

class TagPrintForm(forms.Form):
    tags_to_create = forms.IntegerField(required=False, widget=MDLNumberInput())
    reprint_unassigned = forms.BooleanField(required=False, widget=MDLCheckBox())
    page_template = forms.ModelChoiceField(
        queryset=AssetTagPrintTemplate.objects.all(),
        widget=MDLSelect(),
    )
    tag_template = forms.ModelChoiceField(
        queryset=AssetTagImageTemplate.objects.all(),
        widget=MDLSelect(),
    )
    render_as = forms.ChoiceField(
        choices=(
            ('html', 'HTML'),
            ('pdf', 'PDF'),
        ),
        initial='html',
        widget=MDLSelect(),
    )
    
