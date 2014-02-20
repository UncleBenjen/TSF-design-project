from django.conf.urls import patterns, url
from curriculum import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
		url(r'^about/', views.about, name='index'),
		url(r'^register/$', views.register, name='register'),
		url(r'^login/$', views.user_login, name='login'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^profile/$', views.profile, name='profile'),
		url(r'^departments/$',views.departments, name='departments'),
		url(r'^departments/(?P<department_name_url>\w+)/$',views.department,name='department'),
		)