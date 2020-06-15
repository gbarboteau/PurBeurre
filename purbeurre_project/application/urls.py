from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views # import views so we can use them in urls.


urlpatterns = [
    url(r'^$', views.index, name='index'), # "/store" will call the method "index" in "views.py"
    path("account/", views.account, name='account'),
    path("create-account/", views.create_account, name='create-account'),
    # path("search/", views.search, name='search'),
    url(r'^search/$', views.search, name='search'),
    url(r'aliment/(?P<aliment_id>[0-9]+)/$', views.aliment, name='aliment'),
    path("mesproduits/", views.mesproduits, name='mesproduits'),
    url(r'^add-product/(?P<aliment_id>[0-9]+)/$', views.add_product, name='add_product'),
    url(r'^remove-product/(?P<aliment_id>[0-9]+)/$', views.remove_product, name='remove_product'),
    # path("login/", views.logout_view),
    path("logout/", views.logout_view, name="logout"),
    path("mentionslegales/", views.mentionslegales, name="mentionslegales"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='application/registration/password_reset_form.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='application/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='application/registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='application/registration/password_reset_complete.html'), name='password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)