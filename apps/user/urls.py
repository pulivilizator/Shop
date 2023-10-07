from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.CastomLoginView.as_view(), name='login'),
    path('logout/', views.CastomLogoutView.as_view(), name='logout'),
    path('register/', views.CastomRegisterView.as_view(), name='register'),
    path('reset_passwd/', views.ResetPasswordView.as_view(), name='reset_passwd'),
    path('reset_passwd_done/', views.PasswdResetDone.as_view(), name='reset_passwd_done'),
    path('reset_confirm_passwd/<uidb64>/<token>/', views.PasswdResetConfirm.as_view(), name='password_reset_confirm'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('download/', views.download_file, name='download'),


]