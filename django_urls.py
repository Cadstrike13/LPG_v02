"""
LPG API URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    # Endpoint unique (recommandé pour le frontend)
    path("api/all/", views.api_all, name="api_all"),

    # Endpoints individuels
    path("api/config/", views.api_config, name="api_config"),
    path("api/about/", views.api_about, name="api_about"),
    path("api/values/", views.api_values, name="api_values"),
    path("api/objectives/", views.api_objectives, name="api_objectives"),
    path("api/actions/", views.api_actions, name="api_actions"),
    path("api/board-roles/", views.api_board_roles, name="api_board_roles"),
    path("api/member-types/", views.api_member_types, name="api_member_types"),
    path("api/membership-plans/", views.api_membership_plans, name="api_membership_plans"),
    path("api/contact/", views.api_contact, name="api_contact"),
    path("api/join-statements/", views.api_join_statements, name="api_join_statements"),
]
