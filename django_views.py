"""
LPG API Views - données de la base de données
Tous les endpoints retournent du JSON consommé par le frontend.
"""
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from lpg.models import (
    SiteConfig,
    Value,
    Objective,
    Action,
    BoardRole,
    MemberType,
    MembershipPlan,
    ContactInfo,
    JoinStatement,
)


def _get_site_config():
    return SiteConfig.objects.first()


def _serialize_queryset(queryset):
    return list(queryset.values())


def _build_about_data(config):
    if config is None:
        return {}

    return {
        "title": config.org_name,
        "paragraph1": config.description,
        "paragraph2": config.tagline,
    }


# ─── VIEWS ────────────────────────────────────────────────────────────────────

@require_GET
def api_config(request):
    config = _get_site_config()
    return JsonResponse(model_to_dict(config) if config else {})


@require_GET
def api_about(request):
    config = _get_site_config()
    return JsonResponse(_build_about_data(config))


@require_GET
def api_values(request):
    values = Value.objects.all()
    return JsonResponse({"results": _serialize_queryset(values)})


@require_GET
def api_objectives(request):
    objectives = Objective.objects.all()
    return JsonResponse({"results": _serialize_queryset(objectives)})


@require_GET
def api_actions(request):
    actions = Action.objects.all()
    return JsonResponse({"results": _serialize_queryset(actions)})


@require_GET
def api_board_roles(request):
    board_roles = BoardRole.objects.all()
    return JsonResponse({"results": _serialize_queryset(board_roles)})


@require_GET
def api_member_types(request):
    member_types = MemberType.objects.all()
    return JsonResponse({"results": _serialize_queryset(member_types)})


@require_GET
def api_membership_plans(request):
    membership_plans = MembershipPlan.objects.all()
    return JsonResponse({"results": _serialize_queryset(membership_plans)})


@require_GET
def api_contact(request):
    contact = ContactInfo.objects.first()
    return JsonResponse(model_to_dict(contact) if contact else {})


@require_GET
def api_join_statements(request):
    join_statements = JoinStatement.objects.all()
    return JsonResponse({"results": _serialize_queryset(join_statements)})


@require_GET
def api_all(request):
    """Single endpoint — retourne tout le contenu du site en un appel."""
    config = _get_site_config()
    contact = ContactInfo.objects.first()

    return JsonResponse({
        "config": model_to_dict(config) if config else {},
        "about": _build_about_data(config),
        "values": _serialize_queryset(Value.objects.all()),
        "objectives": _serialize_queryset(Objective.objects.all()),
        "actions": _serialize_queryset(Action.objects.all()),
        "board_roles": _serialize_queryset(BoardRole.objects.all()),
        "member_types": _serialize_queryset(MemberType.objects.all()),
        "membership_plans": _serialize_queryset(MembershipPlan.objects.all()),
        "contact": model_to_dict(contact) if contact else {},
        "join_statements": _serialize_queryset(JoinStatement.objects.all()),
    })
