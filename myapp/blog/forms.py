from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from blog.models import Post, Category




class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=100, required=True)
    email = forms.EmailField(label='Email', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)
    password_confirm = forms.CharField(label='Confirm Password', max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():   # check if email already exists
            raise forms.ValidationError("This email is already registered.")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Password do not matched")

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid Username & Password")



class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=200, required=False)
    content = forms.CharField(label='Content', required=False)
    category = forms.ModelChoiceField(
        label='Category', required=False, queryset=Category.objects.all()
    )
    
    class Meta:
        model = Post
        fields = ("title", "content", "category")

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")

        # custom validation
        if title and len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters")

        if content and len(content) < 10:
            raise forms.ValidationError("content must be at least 10 characters")
    
    def save(self, commit = ...):
        post = super().save(commit)
        img_url = "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg"

        post.img_url = img_url
        if commit:
            post.save()
        return post



    