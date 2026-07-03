from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import (
    MailingListAPIView)

urlpatterns = [
    path('mailing-users/', MailingListAPIView.as_view(), name='organization-settings'),
]
