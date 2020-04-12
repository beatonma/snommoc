"""snommoc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.views.generic import RedirectView
from django.urls import path, include
from .local_urls import urlpatterns as local_urlpatterns

urlpatterns = local_urlpatterns + [
    path('notifications/', include('notifications.urls')),
    path('puk/', include('crawlers.parliamentdotuk.urls')),
    path('api/', include('api.urls')),
    path('auth/', include('social.urls')),
    path('', RedirectView.as_view(url='/about')),
]
