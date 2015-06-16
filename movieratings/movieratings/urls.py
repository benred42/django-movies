"""movieratings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from Movies import views as movie_views
from users import views as user_views
from django.contrib.auth import views as builtin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^top20/$', movie_views.top_20, name="top20"),
    url(r'^top20/number/$', movie_views.top_20_by_number, name="top20_by_number"),
    url(r'^genre/$', movie_views.show_all_genres, name="show_all_genres"),
    url(r'^movie/(?P<movie_id>\d+)$', movie_views.show_movie, name="show_movie"),
    url(r'^rater/(?P<rater_id>\d+)$', movie_views.show_rater, name="show_rater"),
    url(r'^genre/(?P<genre_id>\d+)$', movie_views.show_genre, name="show_genre"),
    url(r'^review/(?P<rating_id>\d+)$', movie_views.show_review, name="show_review"),
    url(r'^register/$', user_views.register_rater, name="user_register"),
    url(r'^login/$', builtin.login, name="login"),
    url(r'^logout/', builtin.logout_then_login, {"login_url": "login"}, name="logout"),
    url(r'^rate/(?P<movie_id>\d*)?$', movie_views.new_rating, name="rate_movie"),
    url(r'^rate/edit/(?P<movie_id>\d*)?$', movie_views.edit_rating, name="edit_rating"),
    url(r'^rate/delete/(?P<movie_id>\d*)?$', movie_views.delete_rating, name="delete_rating"),
    url(r'^accounts/profile/$', movie_views.rater_profile, name="rater_profile"),
]
