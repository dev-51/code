"""cc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app/', include('app.urls')),

    # -------------------------------------------------
    # using parameters with question mark
    # -------------------------------------------------

    # restore database
    # /app/api/?restore=do

    # insert person, company
    # /app/api/?insert=do&cuit=30710647011&account_type=F&name=Roberto&surname=Ruiz&cardid=27066345
    # /app/api/?insert=do&cuit=30117706184&account_type=J&name=Robotics&year=1994

    # update person, company
    # /app/api/?update=do&cuit=30710647011&account_type=F&name=Roberto&surname=Ruiz&cardid=27066345
    # /app/api/?update=do&cuit=30117706184&account_type=J&name=Robotics&year=1994

    # remove person, company
    # /app/api/?remove=do&cuit=30710647011&account_type=F
    # /app/api/?remove=do&cuit=30117706184&account_type=J

    # view person, company
    # /app/api/?view=do&cuit=30710647011&account_type=F
    # /app/api/?view=do&cuit=30117706184&account_type=J

    # view all
    # /app/api/?list=do
    url(r'^app/api/$', views.CRUD.as_view()),

    # -------------------------------------------------
    # using parameters inside url path
    # -------------------------------------------------

    # restore database
    # /app/rest-rs/run/
    url(r'^app/rest-rs/(?P<restore>[a-z]+)/$', views.CRUD.as_view()),

    # insert person
    # /app/rest-ins/run/30710647011/F/Roberto/Ruiz/27066345/
    url(r'^app/rest-ins/(?P<insert>[a-z]+)/(?P<cuit>[0-9]+)/(?P<account_type>[A-Z]{1})/(?P<name>[a-zA-Z]+)/(?P<surname>[a-zA-Z]+)/(?P<cardid>[0-9]+)/$', views.CRUD.as_view()),

    # insert company
    # /app/rest-ins/run/30117706184/J/Robotics/1994/
    url(r'^app/rest-ins/(?P<insert>[a-z]+)/(?P<cuit>[0-9]+)/(?P<account_type>[A-Z]{1})/(?P<name>[a-zA-Z]+)/(?P<year>[0-9]+)/$', views.CRUD.as_view()),

    # update person
    # /app/rest-upt/run/30710647011/F/Roberto/Ruiz/27066345/
    url(r'^app/rest-upt/(?P<update>[a-z]+)/(?P<cuit>[0-9]+)/(?P<account_type>[A-Z]{1})/(?P<name>[a-zA-Z]+)/(?P<surname>[a-zA-Z]+)/(?P<cardid>[0-9]+)/$', views.CRUD.as_view()),

    # update company
    # /app/rest-upt/run/30117706184/J/Robotics/1994/
    url(r'^app/rest-upt/(?P<update>[a-z]+)/(?P<cuit>[0-9]+)/(?P<account_type>[A-Z]{1})/(?P<name>[a-zA-Z]+)/(?P<year>[0-9]+)/$', views.CRUD.as_view()),

    # remove person, company
    # /app/rest-rm/run/30710647011/F/
    # /app/rest-rm/run/30117706184/J/
    url(r'^app/rest-rm/(?P<remove>[a-z]+)/(?P<cuit>[0-9]+)/(?P<account_type>[A-Z]{1})/$', views.CRUD.as_view()),

    # view person, company
    # /app/rest-vw/run/30710647011/F/
    # /app/rest-vw/run/30117706184/J/
    url(r'^app/rest-vw/(?P<show>[a-z]+)/(?P<cuit>[0-9]+)/(?P<account_type>[A-Z]{1})/$', views.CRUD.as_view()),

    # view all
    # /app/rest-ls/run/
    url(r'^app/rest-ls/(?P<list>[a-z]+)/$', views.CRUD.as_view()),
]
