from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'description','bidstart','buynow','comp_image', 'date_end')