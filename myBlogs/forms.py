from django.contrib.auth.models import User
from django import forms
from .models import Post,Comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class createBlog(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','imagespost','is_public',]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
class PostForm(forms.ModelForm):
    is_public = forms.ChoiceField(choices=[(True, 'Public'), (False, 'Không Public')])

    class Meta:
        model = Post
        fields = ['title', 'content','imagespost', 'is_public']