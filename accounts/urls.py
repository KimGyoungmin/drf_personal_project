from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from . import views

app_name = "accounts"

urlpatterns = [
    # 유저 로그아웃 리소스
    path('logout/', views.UserLogoutView.as_view(), name="logout"),
    # jwt 토큰 리소스
    path('login/', views.CustomTokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 회원가입 리소스
    path('', views.UserRegisterationView.as_view(), name='user_registration'),
    # 유저 비밀번호 변경 리소스
    path('password/', views.UserChangePasswordView.as_view(),
         name="user_change_password"),
    # 프로필 리소스
    path('profile/<str:username>/',
         views.UserProfileView.as_view(), name='user_profile'),
]
