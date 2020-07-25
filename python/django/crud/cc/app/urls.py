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
from django.conf.urls import url
from .views import IndexView, AddView, EditView, \
                    RemoveView, DisplayView, RestoreView

urlpatterns = [
    # /app/
    url(r'^$', IndexView.as_view(), name='index'),

    # /app/add/F/ or /app/add/J/
    url(r'add/(?P<account_type>[A-Z]{1})/$', AddView.as_view(), name='add'),

    # /app/edit/
    url(r'edit/(?P<cuit>[0-9]+)/(?P<account_type>[A-Z]{1})/$', EditView.as_view(), name='edit'),

    # /app/remove/
    url(r'remove/(?P<cuit>[0-9]+)/(?P<account_type>[A-Z]{1})/$', RemoveView.as_view(), name='remove'),

    # /app/view/
    url(r'view/(?P<cuit>[0-9]+)/(?P<account_type>[A-Z]{1})/$', DisplayView.as_view(), name='view'),

    # /app/restore/database/
    url(r'restore/database/$', RestoreView.as_view(), name='restore'),
]

