from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import CustomUser
from .form import CustomUserChangeForm, CustomUserCreationForm, VerificationForm
from django.views.generic import UpdateView
from django.contrib.auth import logout
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from .utils import send_verification_email
from django.views.generic import FormView
from django import forms
from django.contrib import messages
import random
from django.utils import timezone
from datetime import timedelta

class MyPageView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'accounts/mypage.html'
    success_url = reverse_lazy('mypage_view')

    def get_object(self, queryset=None):
        return self.request.user
    
class MyPageDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/mypage_view.html'

# アカウント登録ビュー
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('verify_email')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.verification_code = str(random.randint(100000, 999999))  # ← 6桁のコード生成
        user.verification_expiry = timezone.now() + timedelta(minutes=1)
        user.save()

        send_verification_email(user)
        self.request.session['user_email'] = user.email

        return redirect('verify_email')

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')
        
class VerifyEmailView(FormView):
    template_name = 'accounts/verify_email.html'
    form_class = VerificationForm
    success_url = reverse_lazy('login')  # 認証成功後はログイン画面へ

    def form_valid(self, form):
        code = form.cleaned_data['code']
        email = self.request.session.get('user_email')
        try:
            user = CustomUser.objects.get(email=email, verification_code=code)

            # ⏰ 有効期限をチェック
            if timezone.now() > user.verification_expiry:
                user.delete()
                form.add_error('code', '確認コードの有効期限が切れました。もう一度登録してください。')
                return self.form_invalid(form)
            user.is_active = True
            user.save()
            return super().form_valid(form)
        except CustomUser.DoesNotExist:
            form.add_error('code', '確認コードが正しくありません。')
            return self.form_invalid(form)
    


# Create your views here.
