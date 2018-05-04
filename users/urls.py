from django.conf.urls import url

from users import views

urlpatterns = [
	url(r'^my-profile/$', views.MyProfileView.as_view()),
	url(r'^user/$', views.UserList.as_view()),
	url(r'^user/sign-up/$', views.UserSignupView.as_view()),
	url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view()),
	url(r'^change-password/$', views.ChangePasswordView.as_view()),
	url(r'^reset-password/$', views.PasswordResetView.as_view()),
]
