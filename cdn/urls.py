"""home_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import re_path, path

from cdn.views.retrieve import *
from cdn.views.tags import TagsModifyView, TagsView
from cdn.views.upload import *

urlpatterns = [
    path(r'list/', MediaRetrieveListView.as_view()),
    re_path(r'^media/(?P<path>.*)$', MediaRetrieveView.as_view()),
    re_path(r'^upload/(?P<filepath>.*)$', UploadView.as_view()),
    path(r'tag/', TagsView.as_view()),
    re_path(r'^tag/(?P<tag_id>\d+)/$', TagsModifyView.as_view()),
]
