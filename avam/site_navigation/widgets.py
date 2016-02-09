from django import forms
from django.utils.safestring import mark_safe

class MDLWidgetMixin(object):
    widget_template = '''
    <div class="%(div_classes)s">
        %(inner_widget)s
        <label class="mdl-selectfield__label" for="%(id)s">%(label)s</label>
    </div>
    '''
    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(MDLWidgetMixin, self).build_attrs(extra_attrs, **kwargs)
        attrs['class'] = self.inner_classes
        return attrs
    def render_mdl(self, name, attrs, inner_widget):
        return self.widget_template % dict(
            id=attrs['id'],
            div_classes=self.div_classes,
            inner_widget=inner_widget,
            label=self.field.label,
        )

class MDLInputMixin(MDLWidgetMixin):
    div_classes = 'mdl-textfield mdl-js-textfield mdl-textfield--floating-label'
    inner_classes = 'mdl-textfield__input'
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        inner_widget = super(MDLInputMixin, self).render(name, value, final_attrs)
        if inner_widget.endswith(' />'):
            inner_widget = '{0}>'.format(inner_widget[:-3], '>')
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

######## Begin hacky BoundField method override ########

class MDLBoundField(forms.BoundField):
    def as_widget(self, widget=None, attrs=None, only_initial=False):
        """Give every `Widget` instance a reference to its `Field` parent.

        For some reason this is not included in the default implementation,
        but it's necessary to properly render labels within widgets.
        """
        if not widget:
            widget = self.field.widget
        widget.field = self
        return super(MDLBoundField, self).as_widget(widget, attrs, only_initial)

def get_bound_field(self, form, field_name):
    return MDLBoundField(form, self, field_name)

# Yuk, but thanks for the duck typing, python!
forms.Field.get_bound_field = get_bound_field

######## End hacky BoundField method override ##########
