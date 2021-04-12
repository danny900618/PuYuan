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
    path('user/blood/pressure/', views.b_pressure),
    path('user/weight', views.weight),
    path('user/blood/sugar', views.b_sugar),
    path('user/last-upload', views.last_upload),
    path('user/records', views.records),
    path('user/diary', views.diary),
    path('user/diet', views.Diary_diet),
    path('user/care', views.care)

]