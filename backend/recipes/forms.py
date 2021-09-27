from django import forms
from django.forms import ModelForm

from .models import Recipe, Tag


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'pic',
            'ingredients',
            'text',
            'time',
            'tag'
        ]
        tags = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )