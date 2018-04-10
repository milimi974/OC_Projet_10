from django.conf.urls import url

from account.views import save_view, register_view, profile_view, login_view, logout_view, list_view

urlpatterns = [
    url(r'^substitution/$', list_view, name="substitution"),
    url(r'^save/$', save_view, name="save_product"),
    url(r'^register/$', register_view, name="register"),
    url(r'^profile/$', profile_view, name="profile"),
    url(r'^login/$', login_view, name="login"),
    url(r'^logout/$', logout_view, name="logout"),
]