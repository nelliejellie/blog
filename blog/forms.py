from django import forms
from .models import Comment

#creating a post form
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

#creating a comment form from the modelform
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')

#creating a search form 
class SearchForm(forms.Form):
    query = forms.CharField()
