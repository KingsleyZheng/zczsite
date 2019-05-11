from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo

# 用户登录时使用的提交表单
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# 用户注册时使用的表单
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta: #写入数据库的字段
        model = User
        fields = ("username", "email") 

    def clean_password2(self): #拥有clean的对象在检查is_valid的时候都会执行
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("两次输入的密码不一致。")
        return cd['password2']

# 记录用户信息的表单
class UserProfileForm(forms.ModelForm): #如需修改数据库的字段用ModelForm p65
    class Meta: #规定写入数据库的字段
        model = UserProfile
        fields = ("phone", "birth") 

# 记录用户信息的表单2
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school", "company", "profession", "address", "aboutme", "photo")

# 有必要修改的auth_user数据库字段
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)