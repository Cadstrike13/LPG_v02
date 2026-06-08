"""
LPG API URL Configuration
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentification par email
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/password-reset/done/'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/password-reset/complete/'
    ), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Template de la page d'accueil (non utilisé par le frontend React, mais utile pour tests rapides)
    path('', views.home_view, name='home'),

    # Template de l'interface d'administration (protégé)
    path('admin/', views.admin_view, name='admin_interface'),

    # Endpoint unique (recommandé pour le frontend)
    path("api/all/", views.api_all, name="api_all"),

    # Endpoints individuels
    path("api/config/", views.api_config, name="api_config"),
    path("api/about/", views.api_about, name="api_about"),
    path("api/values/", views.api_values, name="api_values"),
    path("api/values/<int:pk>/", views.api_value_detail, name="api_value_detail"),
    path("api/objectives/", views.api_objectives, name="api_objectives"),
    path("api/objectives/<int:pk>/", views.api_objective_detail, name="api_objective_detail"),
    path("api/actions/", views.api_actions, name="api_actions"),
    path("api/actions/<int:pk>/", views.api_action_detail, name="api_action_detail"),
    path("api/board-roles/", views.api_board_roles, name="api_board_roles"),
    path("api/board-roles/<int:pk>/", views.api_board_role_detail, name="api_board_role_detail"),
    path("api/member-types/", views.api_member_types, name="api_member_types"),
    path("api/member-types/<int:pk>/", views.api_member_type_detail, name="api_member_type_detail"),
    path("api/membership-plans/", views.api_membership_plans, name="api_membership_plans"),
    path("api/membership-plans/<int:pk>/", views.api_membership_plan_detail, name="api_membership_plan_detail"),
    path("api/contact/", views.api_contact, name="api_contact"),
    path("api/join-statements/", views.api_join_statements, name="api_join_statements"),
    path("api/join-statements/<int:pk>/", views.api_join_statement_detail, name="api_join_statement_detail"),
    # Users management (simple endpoints for admin UI)
    path("api/auth/users/", views.api_users, name="api_users"),
    path("api/auth/users/<int:pk>/", views.api_user_detail, name="api_user_detail"),
]
