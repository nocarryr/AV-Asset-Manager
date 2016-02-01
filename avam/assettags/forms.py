from django import forms

from site_navigation.widgets import MDLNumberInput, MDLCheckBox, MDLSelect
from assettags.models import (
    AssetTagImageTemplate,
    AssetTagPrintTemplate
)

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
    
class TagScanForm(forms.Form):
    tagcode = forms.CharField(label='Tag Code', max_length=50)
    content_type_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
    )
    object_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
    )
