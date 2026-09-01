from django.urls import path
from .views import index, process_video_view
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('admin-dashboard/detect/',index,name='index'),
    path('stream_video/', process_video_view, name='stream_video'), 
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/reportincident/', views.reportincident_view, name='reportincident'),
    path('dashboard/contactauthorities/', views.contactauthorities_view, name='contactauthorities'),
    path('dashboard/guidelines/', views.guidelines_view, name='guidelines'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin-dashboard/livemonitoring/', views.livemonitoring_view, name='livemonitoring'),
    path('admin-dashboard/alerts/', views.alerts_view, name='alerts'),
    path('admin-dashboard/analysis/', views.analysis_view, name='analysis'),
    path('features/', views.features_view, name='features'),
    path('howitswork/', views.howitswork_view, name='howitswork'),
    path('contact/', views.contact_view, name='contact'),
 #   path('stream_video/', process_video_view, name='stream_video'),
   
]