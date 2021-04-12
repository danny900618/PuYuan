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
    path('friend/code', views.friend_code),
    path('friend/list', views.friend_list),
    path('friend/requests', views.friend_requests),
    path('friend/send', views.friend_send),
    path('<int:friend_data_id>/accept', views.friend_accept),
    path('<int:friend_data_id>/refuse', views.friend_refuse),
    path('<int:friend_data_id>/remove', views.friend_remove),
    path('friend/results', views.friend_results),
    path('friend/remove', views.friend_remove_more) 

]