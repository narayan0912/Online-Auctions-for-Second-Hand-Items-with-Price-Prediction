"""
URL configuration for webapp_auction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from userapp import views as userviews
from postapp import views as postviews
from browseapp import views as browseviews
from bidapp import views as bidviews
urlpatterns = [
    path('', browseviews.home, name='home'),
    path('sell/<str:slug>', bidviews.sell, name='join'),
    path('bid/<str:slug>', bidviews.bid, name='bid'),
    path('browse/', browseviews.browse, name='browse'),
    path('login/', auth_views.LoginView.as_view(template_name='userapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', userviews.register, name='register'),
    path('createprofile/', userviews.create_profile, name='createprofile'),
    path('viewprofile/', userviews.view_profile, name='viewprofile'),
    path('user/<str:username>/', userviews.profile, name='profile'),
    path('post/', postviews.post, name='post'),
    path('predict/', postviews.CarPricePredictView.as_view(), name='predict'),
    path('view/<str:slug>', postviews.view, name='view'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
