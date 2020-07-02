"""likeup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from serach import views as zillow_serach_view
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^auth/google/', include('google_social_auth.urls')),
    url(r'^photoapp/', include('photoapp.urls')),
    path('search/',TemplateView.as_view(template_name="empty.html")),
    path('search/zillow/', zillow_serach_view.GetZillowSearch.as_view(),name='zillow_search')

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

