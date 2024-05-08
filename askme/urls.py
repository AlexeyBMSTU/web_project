"""
URL configuration for askme project.

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
from app import views
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
from django.conf import settings

#from library import views

urlpatterns = [
    path('', views.new_questions, name='base'),                            #новые вопросы
    path('hot', views.best_questions,name='hot'),                          #лучшие вопросы
    path('tag/<str:tag_id>', views.tag_questions, name='tag'),                   #по тегу
    path('question/<str:question_id>', views.OneQuestion, name='question'), 
    path('login', views.log_in, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask', views.ask, name='ask'),
    path('admin/', admin.site.urls),
    path('logout', views.log_out, name='logout'),
    path('profile/edit', views.edit_profile, name='profile'),
    path('profile', views.profile, name='my_profile'),
   # path('test', views.test, name='test'),
   re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = views.pageNotFound
handler500 = views.handler500

