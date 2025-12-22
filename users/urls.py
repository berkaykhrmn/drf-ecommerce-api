from django.urls import path
from .views import RegisterView, LoginView, UserUpdateView, ChangePasswordView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user_register'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('change-password/', ChangePasswordView.as_view(), name='user_change_password'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
]