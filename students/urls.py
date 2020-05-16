# -*- coding: utf-8 -*-
from __future__ import absolute_import


from django.conf.urls import url


from rest_framework.urlpatterns import format_suffix_patterns


from . import views


urlpatterns = format_suffix_patterns([
    url(r'^homepage/$', views.HomeView.as_view(), name='homepage'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^dashboard/list/$',
        views.StudentListView.as_view(),
        name='list'),
    url(r'^dashboard/(?P<pk>[0-9]+)/detail/$',
        views.StudentDetailView.as_view(),
        name='detail'),
    url(r'^dashboard/(?P<pk>[0-9]+)/update/$',
        views.StudentUpdateView.as_view(),
        name='update'),
    url(r'^dashboard/create/$',
        views.StudentCreateView.as_view(),
        name='create'),
    url(r'^dashboard/(?P<pk>[0-9]+)/delete/$',
        views.StudentDeleteView.as_view(),
        name='delete'),
    url(r'^dashboard/logout/$',
        views.LogoutView.as_view(),
        name='logout'),
    url(r'^dashboard/(?P<action>.*)$', views.student_action,
        name='student_action'),
    url(r'^root/$', views.api_root),
    url(r'^list/$',
        views.StudentList.as_view(),
        name='student_list'),
    url(r'^detail/(?P<pk>[0-9]+)/$',
        views.StudentDetail.as_view(),
        name='student_detail'),
])
