from django.urls import path
from . import views, admin_views

app_name = 'ghg'

urlpatterns = [
    # Authentication
    path('login/', views.email_login_view, name='email_login'),
    path('signup/', views.email_signup_view, name='email_signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Main pages
    path('', views.index, name='index'),
    path('data-entry/', views.data_entry, name='data_entry'),
    path('history/', views.emission_history, name='emission_history'),
    path('user-guide/', views.user_guide, name='user_guide'),
    
    # API endpoints
    path('api/calculate/', views.calculate_emission, name='calculate_emission'),
    path('api/user-summary/', views.get_user_emissions_summary, name='user_summary'),
    path('api/country/<str:country_code>/', views.get_country_data, name='country_data'),
    path('api/global/', views.get_global_data, name='global_data'),
    path('api/top-emitters/', views.get_top_emitters, name='top_emitters'),
    
    # Admin (legacy)
    path('admin-login/', admin_views.custom_admin_login, name='admin_login'),
]
