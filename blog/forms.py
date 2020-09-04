from django import forms
from .models import Post


class PostForm(forms.ModelForm): # her using modelForm so we don't need to create form field explicitly
    class Meta:  # we also don't need to use save() method for validation and create instance
        model = Post
        fields = '__all__'

    def clean_slug(self):
        return self.cleaned_data['slug'].lower()  # here return the lowe case slug from cleaned_data(validate data)
