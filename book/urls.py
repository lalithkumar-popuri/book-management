from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CreateBookAPIView

urlpatterns = [
    path('createbook/',CreateBookAPIView.as_view(),name = "CreateBook")
]