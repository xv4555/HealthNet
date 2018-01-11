"""HealthNet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [

    url(r'^prescriptions/?$', views.prescriptions, name='prescriptions'),

    url(r'^patient_transfer/?$', views.patient_transfer, name='patient_transfer'),

    url(r'^patient_transfer/(?P<id>\d+)$', views.patient_transfer, name='patient_transfer_with_id'),

    url(r'^discharge_patient/(?P<id>\d+)$', views.discharge_patient, name='discharge_patient'),

    url(r'^admit_patient/?$', views.admit_patient, name='admit_patient'),

    url(r'^send_message/?$', views.send_message, name='send_message'),

    url(r'^update_message/?$', views.update_message, name='update_message'),

    url(r'^send_message/?$', views.send_message, name='send_message'),

    url(r'^all/$', views.message_center, {'url': 'all'}, name='all'),

    url(r'^read/$', views.message_center, {'url': 'read'}, name='read'),

    url(r'^unread/$', views.message_center, {'url': 'unread'}, name='unread'),

    url(r'^sent/$', views.message_center, {'url': 'sent'}, name='sent'),

    url(r'^compose/$', views.message_center, {'url': 'compose'}, name='compose'),

    url(r'^view_message/(?P<message_id>\d+)$', views.view_message, name='view_message'),

    url(r'^view_log/(?P<log_id>\d+)$', views.view_log, name='view_log'),

    url(r'^view_logs/?$', views.view_logs, name='view_logs'),

    url(r'^add_nurse/?$', views.add_nurse, name='add_nurse'),

    url(r'^add_doctor/?$', views.add_doctor, name='add_doctor'),

    url(r'^add_admin/?$', views.add_admin, name='add_admin'),

    url(r'^add_hospital/?$', views.add_hospital, name='add_hospital'),

    url(r'^view_insurances/?$', views.view_insurances, name='view_insurances'),

    url(r'^view_insurance/(?P<insurance_id>\d+)$', views.view_insurance, name='view_insurance'),

    url(r'^base_dashboard/?$', views.base_dashboard, name='base_dashboard'),

    url(r'^create_appointment/?$', views.create_appointment, name='create_appointment'),

    url(r'^cancel_appointment/(?P<id>\d+)$', views.cancel_appointment, name='cancel_appointment'),

    url(r'^view_appointments/?$', views.view_appointments, name='view_appointments'),

    url(r'^edit_basic_info/?$', views.edit_basic_info, name='edit_basic_info'),

    url(r'^edit_medical_info/?$', views.edit_medical_info, name='edit_medical_info'),

    url(r'^create_account/?$', views.create_account, name='create_account'),

    url(r'^admin/', include(admin.site.urls)),

    url (r'^logout/?$', views.log_out, name='log_out'),

    url(r'^/?$', views.user_login, name='user_login'),

    url(r'^delete_message/(?P<message_id>\d+)$', views.delete_message, name='delete_message'),

    url(r'^reply_to_message/(?P<message_id>\d+)$', views.reply_to_message, name='reply_to_message'),

    url(r'^view_patient/(?P<patient_id>\d+)$', views.view_patient, name='view_patient'),

    url(r'^view_all_patients/?$', views.view_all_patients, name='view_all_patients'),

    url(r'^edit_patient_medical_info/(?P<patient_id>\d+)$', views.edit_patient_medical_info,
        name='edit_patient_medical_info'),

    url(r'^edit_appointment/(?P<id>\d+)$', views.edit_appointment, name='edit_appointment'),

    url(r'^export_data/?$', views.export_data, name='export_data'),

    url(r'^system_statistics/?$', views.system_statistics, name='system_statistics'),

]

