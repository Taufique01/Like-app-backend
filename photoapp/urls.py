from django.urls import path,re_path
from django.conf.urls import include,url
from . import views
urlpatterns = [
       # URLs that do not require a session or valid token
    url(r'^contests/$',  views.ContestView.as_view()),
    url(r'^mycontests/$',  views.MyContestView.as_view()),   
]

