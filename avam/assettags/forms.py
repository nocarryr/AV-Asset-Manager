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
    
