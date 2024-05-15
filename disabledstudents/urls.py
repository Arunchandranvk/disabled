"""
URL configuration for disabledstudents project.

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
from django.urls import path,include
from accounts.views import LoginView,MainHome
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import custom_logout

admin.site.logout = custom_logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',MainHome.as_view(),name='log'),
    path('account/',include("accounts.urls")),
    path('home/',include("home.urls")),
    path('student/',include("student_app.urls")),
    path('game/',include("games.urls")),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
