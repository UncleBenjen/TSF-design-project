from django.conf.urls import patterns, url
from curriculum import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
		url(r'^about/', views.about, name='index'),
		url(r'^register/$', views.register, name='register'),
		url(r'^login/$', views.user_login, name='login'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^profile/$', views.profile, name='profile'),
		url(r'^departments/(?P<department_name_url>\w+)/$',views.department,name='department'),
		url(r'^courses/(?P<course_name_url>\w+)/$',views.course,name='course'),
		url(r'^programs/(?P<program_name_url>\w+)/$',views.program, name='program'),
		url(r'^instances/(?P<course_name_url>\w+)/(?P<instance_date_url>\w+)/$',views.instance,name='instance'),
		url(r'^add_ceab_measurement/$', views.add_ceab_grad,name='add_ceab_grad'),
		url(r'^add_course/$',views.add_course, name = 'add_course'),
		url(r'^add_instance/$',views.add_instance, name = 'add_instance'),
        url(r'^add_concept/$',views.add_concept, name = 'add_concept'),
		url(r'^add_deliverable/$',views.add_deliverable, name = 'add_deliverable'),
		url(r'^add_objective/$',views.add_learning_objective, name = 'add_learning_objective'),
		url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
		url(r'^suggest_course/$', views.suggest_course, name = 'suggest_course'),
		url(r'^suggest_concept/$', views.suggest_concept, name = 'suggest_concept'),
		)