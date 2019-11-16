from django.urls import path,re_path
from django.conf.urls import include,url
from . import views
urlpatterns = [
       # URLs that do not require a session or valid token
    url(r'^get-token/$', views.ConvertTokenView.as_view(),
        name='rest_password_reset'),
    url(r'^revoke-token/$',  views.RevokeTokenView.as_view(),
        name='rest_password_reset_confirm'),    
]
