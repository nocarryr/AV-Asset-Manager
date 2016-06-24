from django import forms

from assettags.models import (
    AssetTagImageTemplate,
    AssetTagPrintTemplate
)

class TagPrintForm(forms.Form):
    tags_to_create = forms.IntegerField(required=False)
    reprint_unassigned = forms.BooleanField(required=False)
    page_template = forms.ModelChoiceField(
        queryset=AssetTagPrintTemplate.objects.all(),
    )
    tag_template = forms.ModelChoiceField(
        queryset=AssetTagImageTemplate.objects.all(),
    )
    render_as = forms.ChoiceField(
        choices=(
            ('html', 'HTML'),
            ('pdf', 'PDF'),
        ),
        initial='html',
    )
    pdf_preview = forms.BooleanField(required=False)

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
