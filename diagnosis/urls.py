from django.urls import path
from diagnosis import views

urlpatterns = [
    path('diagnosis_picture/', views.DiagnosisPictureView.as_view()),

]