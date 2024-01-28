from django import forms
from .models import Post

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['postCategory', 'title', 'text','author']

class NewsPostCreationForm(PostCreationForm):
    class Meta(PostCreationForm.Meta):
        widgets = {
            'categoryType': forms.HiddenInput(attrs={'value': Post.NEWS}),
        }

class ArticlePostCreationForm(PostCreationForm):
    class Meta(PostCreationForm.Meta):
        widgets = {
            'categoryType': forms.HiddenInput(attrs={'value': Post.ARTICLE}),
        }


class NewsPostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['postCategory', 'title', 'text', 'author', 'categoryType']
        widgets = {'categoryType': forms.HiddenInput()}

class ArticlePostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['postCategory', 'title', 'text', 'author', 'categoryType']
        widgets = {'categoryType': forms.HiddenInput()}

