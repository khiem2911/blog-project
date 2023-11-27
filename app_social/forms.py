from .models import CustomUser,Post,Comment,Like,Friendship,Group,GroupPost,ReplyComment
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm


class createGroup(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name','description','group_picture','imgcover']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'images', 'video']

class GroupPostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = ['content','images']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = ReplyComment
        fields = ['text']

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES, widget=forms.RadioSelect)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'first_name' ,'last_name','email', 'date_of_birth', 'gender', 'bio', 'avatar', 'lives')
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

        
class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1','new_password2')