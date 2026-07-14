from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
# from .views import login_view,signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portal/', include("portal.urls")),
    path('portal/admin/', include("admin_api.urls")),
    path('api/', include('service_api.urls')),
]
