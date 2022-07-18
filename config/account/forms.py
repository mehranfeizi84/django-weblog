from django import forms
from django.urls import reverse_lazy
from .models import User
from django.contrib.auth.views import LoginView
from django.core import validators


# custom form for profile view and show custom fields in profile template
class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        user = kwargs.pop('user')

        super(ProfileForm, self).__init__(*args, **kwargs)

        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['username'].help_text = None
            self.fields['image'].help_text = "یه عکس واسه پروفایلت انتخاب کن"
            self.fields['email'].disabled = True
            self.fields['is_author'].disabled = True
            self.fields['special_user'].disabled = True
        else:
            self.fields['username'].help_text = None


    class Meta:
        model = User
        fields = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_author',
        'special_user',
        'image',
    ]


# custom login form and changed success_url
class CustomLogin(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_author:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')


# custom form for register view and hadle errors
class RegisterForm(forms.Form):
    user_name = forms.CharField(
        label='نام کاربری:',
        validators=[
            validators.MaxLengthValidator(limit_value=20,message="اسم وارد شده نباید بیشتر از 20 کاراکتر باشد")
        ]
    )

    email = forms.EmailField(
        label='ایمیل:',
        validators=[
            validators.MinLengthValidator(limit_value=12,message="ایمیل وارد شده خیلی کوتاه است"),
            validators.EmailValidator(message="ایمیل وارد شده معتبر نمیباشد")
        ]
    )

    password = forms.CharField(
        label='کلمه ی عبور:'
    )

    re_password = forms.CharField(
        label='کلمه ی عبور دوباره:'
    )

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exists_user = User.objects.filter(username=user_name).exists()
        
        if is_exists_user:
            raise forms.ValidationError("این کاربر قبلا ثبت نام کرده است")
        
        return user_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exists_email = User.objects.filter(email=email).exists()
        
        if is_exists_email:
            raise forms.ValidationError("این ایمیل قبلا ثبت نام کرده است")
        
        if len(email) < 10:
            raise forms.ValidationError("ایمیل خیلی کوتاه است")

        return email

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')

        if password != re_password:
            raise forms.ValidationError("رمز عبور اشتباه است")
        
        return password
