from django.urls import path
from .views import MyPageView, LoginView, LogoutView, SignUpView, CustomLogoutView, MyPageDetailView

urlpatterns = [
    path('mypage/', MyPageView.as_view(), name='mypage'),
    path('mypage/view/', MyPageDetailView.as_view(), name='mypage_view'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]