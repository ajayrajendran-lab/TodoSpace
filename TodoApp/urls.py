"""
URL configuration for TodoApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name="register"),
    path('signin/',views.SignInView.as_view(),name="signin"),
    path('index/',views.IndexView.as_view(),name="index"),
    path('signout/',views.SignOutView.as_view(),name="signout"),
    path('todo/add/',views.TodoCreateView.as_view(),name="todo-add"),
    path('todo/<int:pk>/remove/',views.TodoDeleteView.as_view(),name="todo-remove"),
    path('todo/<int:pk>/change/',views.TodoUpdateView.as_view(),name="todo-change"),
    path('todo/all/',views.TodoListView.as_view(),name="todo-all"),
    path('',views.HomeView.as_view(),name="home"),
    path('api/',include('api.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
