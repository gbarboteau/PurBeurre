from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views # import views so we can use them in urls.


urlpatterns = [
    url(r'^$', views.index, name='index'), # "/store" will call the method "index" in "views.py"
    path("account/", views.account, name='account'),
    path("create-account/", views.create_account, name='create-account'),
    # path("search/", views.search, name='search'),
    url(r'^search/$', views.search, name='search'),
    url(r'aliment/(?P<aliment_id>[0-9]+)/$', views.aliment),
    path("mesproduits/", views.mesproduits),
    url(r'^add-product/$', views.add_product, name='add_product'),
    # path("login/", views.logout_view),
    path("logout/", views.logout_view),
    path("mentionslegales/", views.mentionslegales),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)