from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Hero


class AddArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'choose a category'

    class Meta:
        model = Hero
        fields = ['title', 'slug', 'content', 'image', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'id': "inputTitle", 'placeholder': "title", 'class': "form-input"}),
            'slug': forms.TextInput(attrs={'id': "inputUrl", 'placeholder': "url", 'class': "form-control"}),
            # 'content': forms.Textarea(attrs={'id': "inputContent", 'placeholder': "article", 'class': "form-control"}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        print(title)
        if len(title) > 200:
            return ValidationError('Title is too long')
        return title

    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': "inputContent",
            'placeholder': "write article"
        }), label='Descriptions')

    # title = forms.CharField(
    #     max_length=250,
    #     label='Title',
    #     widget=forms.TextInput(attrs={
    #         'id': "inputTitle",
    #         'placeholder': "title",
    #         'cols': 60,
    #         'class': "form-control",
    #     }))
    # slug = forms.SlugField(
    #     max_length=200,
    #     label='Slug',
    #     widget=forms.TextInput(attrs={
    #         'id': "inputUrl",
    #         'placeholder': "url",
    #         'class': "form-control",
    #     }))
    # content = forms.CharField(
    #     widget=forms.Textarea(attrs={
    #         'id': "inputContent",
    #         'placeholder': "write article"
    #     }), label='Descriptions')
    # is_published = forms.BooleanField(initial=True)
    # categoty = forms.ModelChoiceField(queryset=Category.objects.all())