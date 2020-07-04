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
]
