"""jobs URL Configuration

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
from . import views
urlpatterns = [
    #url(r'^admin/', admin.site.urls),
	url(r'^index$', views.index),
	url(r'^showjobs$', views.showjobs,name="showjobs"),
	url(r'^showjobs/liepin$', views.showjobs_liepin, name="showjobs_liepin"),
	url(r'^showjobs/qiancheng$', views.showjobs_qiancheng, name="showjobs_qiancheng"),
	url(r'^showjobs/zhilian$', views.showjobs_zhilian, name="showjobs_zhilian"),
]
