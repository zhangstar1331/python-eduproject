from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile,EmailVerifyCode
import re
class UserRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=3,max_length=15,error_messages={
        'required':'密码必须填写',
        'min_length':'密码不得小于3位',
        'max_length':'密码不得大于15位'
    })
    captcha = CaptchaField(error_messages={
        'invalid': '验证码错误'
    })

class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=3,max_length=15,error_messages={
        'required':'密码必须填写',
        'min_length':'密码不得小于3位',
        'max_length':'密码不得大于15位'
    })

class UserForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={
        'invalid': '验证码错误'
    })

class UserResetForm(forms.Form):
    password = forms.CharField(required=True,min_length=3,max_length=15,error_messages={
        'required':'密码必须填写',
        'min_length':'密码不得小于3位',
        'max_length':'密码不得大于15位'
    })
    password1 = forms.CharField(required=True, min_length=3, max_length=15)

class UserChangeImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class UserChangeInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','birthday','gender','address','phone']

class UserChangeEmailForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email']
    def clean_email(self):
        email = self.cleaned_data['email']
        com = re.compile('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
        if com.match(email):
            return email
        else:
            raise forms.ValidationError('邮箱格式错误')
class UserResetEmailForm(forms.ModelForm):
    class Meta:
        model = EmailVerifyCode
        fields = ['email','code']