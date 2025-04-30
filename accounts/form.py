from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="メールアドレス")
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        help_text="8文字以上のパスワードを入力してください。",
    )
    password2 = forms.CharField(
        label="パスワード（確認）",
        widget=forms.PasswordInput,
        help_text="確認のため、同じパスワードをもう一度入力してください。",
    )

    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('address', 'postal_code', 'phone_number')
        labels = {
            'address': '住所',
            'postal_code': '郵便番号',
            'phone_number': '電話番号',
        }

class VerificationForm(forms.Form):
    code = forms.CharField(label='確認コード', max_length=6)