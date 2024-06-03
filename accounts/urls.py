from django.urls import path,include
from .views import (UserRegistrationView,UserLoginView,UserProfileView, UserChangePasswordView, 
                    SendResetPasswordEmailView, UserPasswordResetView)

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name = "register"),
    path('login/',UserLoginView.as_view(),name = "login"),
    path('profile/',UserProfileView.as_view(),name = "profile"),
    path('ChangePassword/',UserChangePasswordView.as_view(),name = "Change Password"),
    path('send-password-reset-email',SendResetPasswordEmailView.as_view(),name="send-password-reset-email"),
    path('ResetPassword/<uid>/<token>',UserPasswordResetView.as_view(),name="Reset password"),

]