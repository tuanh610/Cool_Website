"""Cool_Website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .settings import STATIC_URL, STATIC_ROOT
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
# Login url
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='Login'),
    # Logout url
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='Logout'),
    #Register URL
    path('register/', views.register, name='Register'),
    path('about/', views.about, name='about'),
    path('', views.home, name='home'),
    # Operation result page, use to show error after operation fail
    path('request_result/?error=<str:error>', views.request_result, name='request_result_error'),
    # Operation result page, use to show status after operation success
    path('request_result/?status=<str:status>', views.request_result, name='request_result_ok'),
] + static(STATIC_URL, document_root=STATIC_ROOT)
