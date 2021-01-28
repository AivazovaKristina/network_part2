from django import forms
from django.forms import (ChoiceField, ModelChoiceField, ModelForm, Textarea,
                          TextInput)

from .models import Comment, Group, Post

# from users.models import Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image',]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


