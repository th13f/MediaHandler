from django import forms
from tagging_autocomplete.widgets import TagAutocomplete
from tagging.forms import TagField

__author__ = 'th13f'


class TagsForm(forms.Form):
    tags = TagField(widget=TagAutocomplete())