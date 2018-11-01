from django.conf.urls import url
from api import views

urlpatterns = [
	url(r'^crisis/$', views.get_crisis_list),
	url(r'^crisis/create/$', views.create_crisis),
	url(r'^crisis/(?P<crisis_id>[0-9]+)/$', views.get_crisis_detail),
	url(r'^crisis/(?P<crisis_id>[0-9]+)/edit/$', views.edit_crisis),
	url(r'^crisis/(?P<crisis_id>[0-9]+)/create_action_update/$', views.create_action_update),
	url(r'^crisis/(?P<crisis_id>[0-9]+)/update_status/$', views.update_crisis_status),
	url(r'^crisis/(?P<crisis_id>[0-9]+)/notify_public/$', views.notify_public),
]