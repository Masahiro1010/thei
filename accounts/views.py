from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .models import CustomUser
from .form import CustomUserChangeForm, CustomUserCreationForm
from django.views.generic import UpdateView
from .form import CustomUserChangeForm
from django.contrib.auth import logout
from django.views import View
from django.shortcuts import redirect

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
    success_url = reverse_lazy('login')

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')
    


# Create your views here.
