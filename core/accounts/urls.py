from django.urls import path
from .views import UserRegisterView, UserUpdateView
from .tokens import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', CustomTokenObtainPairView.as_view(), name='user_login'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
]