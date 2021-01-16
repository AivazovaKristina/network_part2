from django.forms import ModelForm, TextInput, Textarea, ChoiceField, ModelChoiceField
from .models import Post,Group



class PostForm(ModelForm):
    class Meta:
        model = Post
        #group = ModelChoiceField(queryset=Group.objects.all(), to_field_name=None, required=False)

        fields = ('group', 'text')
        # widgets = {
        #     "text": Textarea(attrs={
        #         'class':'form-control',
        #         'placeholder':"Введите текст"
        #     }),
        # }
