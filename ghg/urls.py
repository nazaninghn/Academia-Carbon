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
    path('test-report/', views.test_report_feature, name='test_report_feature'),
    path('test-custom-factor/', views.test_custom_factor_feature, name='test_custom_factor_feature'),
    
    # API endpoints
    path('api/calculate/', views.calculate_emission, name='calculate_emission'),
    path('api/user-summary/', views.get_user_emissions_summary, name='user_summary'),
    path('api/dashboard/', views.dashboard_api, name='dashboard_api'),
    path('api/analysis/emissions/summary/', views.emissions_summary_api, name='emissions_summary_api'),
    path('api/report-extra/', views.report_extra_info_api, name='report_extra_info_api'),
    path('api/country/<str:country_code>/', views.get_country_data, name='country_data'),
    path('api/global/', views.get_global_data, name='global_data'),
    path('api/top-emitters/', views.get_top_emitters, name='top_emitters'),
    path('api/suppliers/', views.get_suppliers, name='get_suppliers'),
    path('api/suppliers/add/', views.add_supplier, name='add_supplier'),
    
    # Custom emission factors
    path('api/custom-factors/', views.get_custom_factors, name='get_custom_factors'),
    path('api/custom-factors/add/', views.add_custom_factor, name='add_custom_factor'),
    path('api/custom-factors/calculate/', views.calculate_with_custom_factor, name='calculate_custom_factor'),
    path('api/materials/request/', views.request_new_material, name='request_material'),
    
    # Emission records management
    path('api/emission-records/<int:record_id>/', views.get_emission_record, name='get_emission_record'),
    path('api/emission-records/<int:record_id>/update/', views.update_emission_record, name='update_emission_record'),
    path('api/emission-records/<int:record_id>/delete/', views.delete_emission_record, name='delete_emission_record'),
    
    # Export reports
    path('api/export-report/<str:scope>/', views.export_emission_report, name='export_report'),
    
    # Analysis pages
    path('analysis/', views.analysis_index, name='analysis_index'),
    path('analysis/emissions/', views.analysis, name='analysis'),
    path('api/analysis/scope-distribution/', views.analysis_scope_distribution, name='analysis_scope_distribution'),
    path('api/analysis/monthly-trends/', views.analysis_monthly_trends, name='analysis_monthly_trends'),
    path('api/analysis/top-sources/', views.analysis_top_sources, name='analysis_top_sources'),
    
    # Emissions analysis (Carbondeck-style)
    path('emissions/', views.emissions, name='emissions'),
    path('api/emissions/data/', views.emissions_data_api, name='emissions_data_api'),
    path('api/emissions/export/', views.emissions_export_api, name='emissions_export_api'),
    
    # Admin (legacy)
    path('admin-login/', admin_views.custom_admin_login, name='admin_login'),
]
