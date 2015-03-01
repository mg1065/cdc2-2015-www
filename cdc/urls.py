from django.conf.urls import patterns, include, url
from cdc import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^about$', views.about, name='about'),
    url(r'^testimonials$', views.testimonials, name='testimonials'),
    url(r'^testimonials/(?P<t_id>\d+)/delete$', views.testimonials_delete, name='testimonials_delete'),
    url(r'^form$', views.form, name='form'),
    url(r'^accounts/login$', views.login_view, name='login'),
    url(r'^accounts/logout$', views.logout_view, name='logout'),
    url(r'^accounts/home$', views.account_home, name='account'),
    url(r'^accounts/settings$', views.settings, name='settings'),
    url(r'^accounts/upload$', views.upload, name='upload'),
    url(r'^accounts/filings$', views.filings, name='filings'),
    url(r'^accounts/reports$', views.reports, name='reports'),
    url(r'^accounts/success$', views.success, name='success'),

    url(r'^accounts/login/admin$', views.login_admin, name='login_admin'),
    url(r'^accounts/admin$', views.admin_dashboard, name='admin_new'),
    url(r'^accounts/admin/old$', views.admin, name='admin'),
    url(r'^accounts/admin/user/reset$', views.admin_password_reset, name='admin_password_reset'),
    url(r'^accounts/admin/user/delete$', views.admin_delete_user, name='admin_delete_user'),
    url(r'^accounts/admin/user/create$', views.admin_new_user, name='admin_new_user'),
    url(r'^accounts/admin/user/create/admin$', views.admin_new_admin, name='admin_new_admin'),
    url(r'^accounts/admin/user/files$', views.admin_list_user_files, name='admin_list_user_files'),
)
