from django.conf.urls import url

from product import views

urlpatterns = [
    url('search/', views.search, name="search"),
    url('autocomplete/$', views.terms, name="product_terms"),
    url('show/(?P<id>[0-9]+)$', views.show, name="show"),
]
