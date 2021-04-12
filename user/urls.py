"""pythontest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('register/', views.register),
    #path('register/check/', views.recheck),
    path('auth/', views.login),
    path('verification/send/', views.send),
    path('verification/check/', views.check),
    path('password/forgot/', views.ForgetPwd),
    path('password/reset/', views.ResetPwd),
    path('user', views.User_set),
    path('user/default', views.User_defult),
    path('user/setting', views.User_setting),
    path('user/a1c', views.hba1c),
    path('user/medical', views.med_inf),
    path('user/drug-used', views.drug_inf),
    path('notification', views.notification),
    path('share', views.share),
    path('share/<int:relation_type>', views.share_check),
    path('news', views.newnews),
    path('user/badge', views.badge)
]