"""codingalphas URL Configuration

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from Core import views as user_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('Core.urls')),
    path("discuss/",include('discuss.urls')),
    path('ckeditor/',include("ckeditor_uploader.urls")),
    path("coding/",include("coding.urls")),
    path("blog/",include("blogs.urls")),
    path("notebook/",include("Notebook.urls")),
    path("playground/",include("Playground.urls")),
    path('login/', auth_views.LoginView.as_view(template_name='Core/snippets/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    # since the logged in user can also access password reset form, we are overriding inbuilt PasswordResetView in the views.py file
    path('password_reset/', user_views.MyPasswordResetView.as_view(template_name='Core/snippets/password_reset.html'), name="password_reset"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
