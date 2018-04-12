from django.conf.urls import url

from users import views

urlpatterns = [
	url(r'^user/$', views.UserList.as_view()),
	url(r'^user/sign-up/$', views.UserSignupView.as_view()),
	url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view()),
]
