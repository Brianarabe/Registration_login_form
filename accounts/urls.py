from django.urls import path
from . import views

urlpatterns = [
    # Home and Authentication URLs
    path('', views.home, name='home'),
    path('register/broker/', views.register_broker, name='broker_register'),
    path('register/agent/', views.register_agent, name='agent_register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Broker URLs
    path('broker/dashboard/', views.broker_dashboard, name='broker_dashboard'),
    path('broker/profile/', views.broker_profile, name='broker_profile'),
    path('broker/properties/', views.broker_properties, name='broker_properties'),
    path('broker/properties/<int:property_id>/', views.broker_property_detail, name='broker_property_detail'),
    
    # Agent URLs
    path('agent/dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('agent/profile/', views.agent_profile, name='agent_profile'),
    path('agent/properties/', views.agent_properties, name='agent_properties'),
    path('agent/properties/<int:property_id>/', views.agent_property_detail, name='agent_property_detail'),
]