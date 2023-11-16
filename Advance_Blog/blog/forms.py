from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# class SignupForm(forms.Form):
#     author=forms.CharField(
#         max_length=30,
#         widget=forms.TextInput(attrs={"class":"form-control","placeholder":"user_name"})
#     )
#     password=forms.CharField(
#         min_length=8,
#         max_length=15,
#         widget=forms.TextInput(attrs={"class":"form-control","placeholder":"password"})
#     )
#     confirm_password=forms.CharField(
#         min_length=8,
#         max_length=15,
#         widget=forms.TextInput(attrs={"class":"form-control","placeholder":"password_confirm"})
#     )
    
# class LoginForm(forms.Form):
#     author=forms.CharField(
#         max_length=30,
#         widget=forms.TextInput(attrs={"class":"form-control","placeholder":"user_name"})
#     )
#     password=forms.CharField(
#         max_length=15,
#         widget=forms.TextInput(attrs={"class":"form-control","placeholder":"password"})
#     )
class NewUserForm(UserCreationForm):
    email=forms.EmailField(required=True)
    
    class Meta:
        model=User
        fields=("username","email","password1","password2")
        
        def save(self,commit=True):
            user=super(NewUserForm,self).save(commit=False)
            user.email=self.cleaned_data["email"]
            if commit:
                user.save()
            return user

class CommentForm(forms.Form):
    author=forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={"class":"form-control1","placeholder":"your name"})
    )
    body=forms.CharField(
        widget=forms.Textarea(attrs={"class":"form-control1","placeholder":"Leave your comment!"})
    )
    
class PostForm(forms.Form):
    title=forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class":"form-control2","placeholder":"Post Title"}),
    )
    body=forms.CharField(
        widget=forms.Textarea(attrs={"class":"form-control2","placeholder":"Create Your Post"}),
    )
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control2"}),
        required=False  # Optional field
    )
