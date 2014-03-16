from django.conf.urls import patterns, url
from curriculum import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
		url(r'^about/', views.about, name='index'),
		url(r'^register/$', views.register, name='register'),
		url(r'^login/$', views.user_login, name='login'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^profile/$', views.profile, name='profile'),
		url(r'^course_list/$', views.all_courses, name='all_courses'),
		url(r'^departments/(?P<department_name_url>\w+)/$',views.department,name='department'),
		url(r'^courses/(?P<course_name_url>\w+)/$',views.course,name='course'),
		url(r'^programs/(?P<program_name_url>\w+)/$',views.program, name='program'),
		url(r'^options/(?P<option_name_url>\w+)/$',views.option,name='option'),
		url(r'^instances/(?P<course_name_url>\w+)/(?P<instance_date_url>\w+)/$',views.instance,name='instance'),
		url(r'^concepts/(?P<concept_name_url>\w+)/$', views.concept, name='concept'),
		url(r'^add_ceab_measurement/(?P<course_url>\w+)/(?P<date_url>\w+)/$', views.add_ceab_grad,name='add_ceab_grad'),
		url(r'^add_scores/(?P<course_url>\w+)/(?P<date_url>\w+)/(?P<ceab_url>\w+)/$', views.add_measurement,name='add_measurement'),
		url(r'^add_course/$',views.add_course, name = 'add_course'),
		url(r'^add_instance/$',views.add_instance, name = 'add_instance'),
		url(r'^add_professor/(?P<course_url>\w+)/(?P<date_url>\w+)/$',views.add_professor, name = 'add_professor'),
		url(r'^add_assistant/(?P<course_url>\w+)/(?P<date_url>\w+)/$',views.add_assistant, name = 'add_assistant'),
		url(r'^add_textbook/(?P<course_url>\w+)/(?P<date_url>\w+)/$',views.add_textbook, name = 'add_textbook'),
		url(r'^add_students/(?P<course_url>\w+)/(?P<date_url>\w+)/$',views.add_student_group, name = 'add_student_group'),
		url(r'^add_deliverable/(?P<course_url>\w+)/(?P<date_url>\w+)/$',views.add_deliverable, name = 'add_deliverable'),
		url(r'^add_objective/(?P<course_url>\w+)/(?P<date_url>\w+)/$',views.add_learning_objective, name = 'add_learning_objective'),
		url(r'^add_concept_search/(?P<course_url>\w+)/(?P<date_url>\w+)/$', views.add_concept_search, name='add_concept_search'),
		url(r'^add_concept/(?P<course_url>\w+)/(?P<date_url>\w+)/$',views.add_concept_to_instance, name = 'add_concept_to_instance'),
		url(r'^link_concept/(?P<course_url>\w+)/(?P<date_url>\w+)/(?P<name_url>\w+)/$',views.link_concept, name = 'link_concept'),
		url(r'^edit_concept_relation/(?P<course_url>\w+)/(?P<date_url>\w+)/(?P<concept_url>\w+)/$', views.edit_concept_relation, name='edit_concept_relation'),
		url(r'^add_concept/',views.add_concept, name = 'add_concept'),
		url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
		url(r'^suggest_concept_add/$', views.suggest_concept_add, name = 'suggest_concept_add'),
		url(r'^suggest_child_concept_add/$', views.suggest_child_concept_add, name = 'suggest_child_concept_add'),
		url(r'^suggest_course/$', views.suggest_course, name = 'suggest_course'),
		url(r'^suggest_concept/$', views.suggest_concept, name = 'suggest_concept'),
		url(r'^add_cohort/(?P<program_stream_url>\w+)/$', views.add_cohort, name='add_cohort'),
		url(r'^contact_hours_cohort/(?P<id_url>\w+)/$', views.contact_hours_cohort, name='contact_hours_cohort'),
		url(r'^ceab_grad/(?P<course_url>\w+)/(?P<date_url>\w+)/(?P<ceab_url>\w+)/$', views.ceab_grad, name='ceab_grad'),
		url(r'^AU/(?P<program_url>\w+)/(?P<year_url>\w+)/$', views.get_program_au, name='get_program_au'),
		url(r'^select_program_for_au/$', views.get_programs, name='get_program_for_au'),
		url(r'^add_child_concept/(?P<concept_url>\w+)/(?P<child_url>\w+)/$', views.add_child_concept, name='add_child_concept'),
		url(r'^add_child_concept_search/(?P<concept_url>\w+)/$', views.add_child_concept_search, name='add_child_concept_search'),
		)