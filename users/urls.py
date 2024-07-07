from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('signup/', views.SignupView.as_view()),
    path('verify_password/', views.ForgetPassowrdVerificationView.as_view()),
    path('my_profile/', views.MyProfileView.as_view()),
    path('my_profile_picture/', views.ProfilePictureView.as_view()),
    path('forgot_password/', views.ForgetPasswordView.as_view()),
]