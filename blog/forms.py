from .models import Comment, Post
from django import forms

from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'slug')
        widgets = {
            'content': SummernoteWidget(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'content': SummernoteWidget(),
        }