from django.urls import path,re_path
from django.conf.urls import include,url
from . import views
urlpatterns = [
       # URLs that do not require a session or valid token
    url(r'^contests/$',  views.ContestView.as_view()),
    url(r'^mycontests/$',  views.MyContestView.as_view()),   
    url(r'^image/upload/$', views.upload_pic, name='upload_pic'),
    url(r'^feed/items/$',  views.GetPhotoFeed.as_view()),   
    url(r'^photo/liked/$',  views.PhotoLike.as_view()),
    url(r'^join/contest/$',  views.ContestPayment.as_view()),
    url(r'^pay/verify/$',  views.VerifyPayment.as_view()),
    url(r'^contest_history/$',  views.ContestHistoryView.as_view()),
    url(r'^userearning/$',  views.UserEarningView.as_view()),
]

