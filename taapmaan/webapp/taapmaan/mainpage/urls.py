# mainpage.urls.py
from django.conf.urls import url
from mainpage import views


urlpatterns = [
    url(r'^$', views.graph),
    url(r'^about/$', views.about),
    url(r'^logs/$', views.logs),
    url(r'^settings/sensor$', views.sensor_settings),
    url(r'^settings/webapp', views.webapp_settings),
    url(r'^settings/rule$', views.rule_settings),

    url(r'^about/ajax-about$', views.ajax_about),
    url(r'^query-graph/', views.graph),
]
