"""
URL configuration for Doctor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from Clinic.views import show_table, home, appointment_page, login_page, reg_page,log_out


urlpatterns = [
    path('', home, name='index'),
    path('home/', home, name='home'),
    path('admin/', admin.site.urls),
    path('table/', show_table, name='table'),
    path('appoint/', appointment_page, name='appoint'),
    path('create_response/', appointment_page),
    path('login/', login_page, name='login'),
    path('sign_up/', reg_page, name='register'),
    path('logout/', log_out, name='logout')
]
