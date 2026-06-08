"""
LPG API Views - données de la base de données
Tous les endpoints retournent du JSON consommé par le frontend.
"""
import json

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

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

User = get_user_model()

def home_view(request):
    """Simple template pour tester que le serveur fonctionne (non utilisé par React)."""
    return render(request, 'index.html')


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autofocus': True, 'autocomplete': 'email'})
    )
    password = forms.CharField(
        label='Mot de passe',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )
    remember_me = forms.BooleanField(
        label='Rester connecté',
        required=False,
        initial=False,
    )

    error_messages = {
        'invalid_login': 'Email ou mot de passe incorrect.',
        'inactive': 'Ce compte est inactif.',
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(self.error_messages['inactive'], code='inactive')

    def get_user(self):
        return self.user_cache


@login_required(login_url='login')
def admin_view(request):
    """Template pour l'interface d'administration (non utilisé par React)."""
    return render(request, 'lpg-admin.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_interface')

    if request.method == 'POST':
        form = EmailAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if form.cleaned_data.get('remember_me'):
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                request.session.set_expiry(0)
            next_url = request.POST.get('next') or request.GET.get('next') or reverse('admin_interface')
            return redirect(next_url)
    else:
        form = EmailAuthenticationForm(request)

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


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


def _parse_json_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ValueError("JSON invalide")


def _serialize_model(instance):
    return model_to_dict(instance)


def _serialize_config(config):
    """Serialize SiteConfig, converting ImageField to string URL."""
    if not config:
        return {}
    data = model_to_dict(config)
    # Convert ImageField to URL string
    if config.logo_url:
        data['logo_url'] = config.logo_url.url
    else:
        data['logo_url'] = ""
    return data

OBJECTIVE_FIELDS = ["number", "title", "description", "icon"]
ACTION_FIELDS = ["title", "description", "icon", "order"]
BOARD_ROLE_FIELDS = ["title", "order"]
MEMBER_TYPE_FIELDS = ["title", "description", "icon", "order"]
MEMBERSHIP_PLAN_FIELDS = ["plan_type", "price", "currency", "period", "title", "subtitle", "benefits", "is_featured", "order"]
CONTACT_FIELDS = ["address", "phones", "email", "status"]
JOIN_STATEMENT_FIELDS = ["text", "order"]
SITE_CONFIG_FIELDS = ["org_name", "acronym", "tagline", "description", "founded_year", "city", "country", "bureau_members_count", "objectives_count", "duration_label", "motto", "motto_label", "logo_url", "cta_label"]


def _apply_updates(instance, data, allowed_fields):
    for field, value in data.items():
        if field in allowed_fields:
            setattr(instance, field, value)
    instance.save()
    return instance


# ─── VIEWS ────────────────────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["GET", "PUT"])
def api_config(request):
    if request.method == "GET":
        config = _get_site_config()
        return JsonResponse(_serialize_config(config))

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    config, _ = SiteConfig.objects.update_or_create(pk=1, defaults={k: v for k, v in payload.items() if k in SITE_CONFIG_FIELDS})
    return JsonResponse(_serialize_config(config))


@require_GET
def api_about(request):
    config = _get_site_config()
    return JsonResponse(_build_about_data(config))


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_values(request):
    if request.method == "GET":
        values = Value.objects.all()
        return JsonResponse({"results": _serialize_queryset(values)})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    value = Value.objects.create(**{k: v for k, v in payload.items() if k in VALUE_FIELDS})
    return JsonResponse(_serialize_model(value), status=201)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_objectives(request):
    if request.method == "GET":
        objectives = Objective.objects.all()
        return JsonResponse({"results": _serialize_queryset(objectives)})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    objective = Objective.objects.create(**{k: v for k, v in payload.items() if k in OBJECTIVE_FIELDS})
    return JsonResponse(_serialize_model(objective), status=201)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_actions(request):
    if request.method == "GET":
        actions = Action.objects.all()
        return JsonResponse({"results": _serialize_queryset(actions)})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    action = Action.objects.create(**{k: v for k, v in payload.items() if k in ACTION_FIELDS})
    return JsonResponse(_serialize_model(action), status=201)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_board_roles(request):
    if request.method == "GET":
        board_roles = BoardRole.objects.all()
        return JsonResponse({"results": _serialize_queryset(board_roles)})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    board_role = BoardRole.objects.create(**{k: v for k, v in payload.items() if k in BOARD_ROLE_FIELDS})
    return JsonResponse(_serialize_model(board_role), status=201)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_member_types(request):
    if request.method == "GET":
        member_types = MemberType.objects.all()
        return JsonResponse({"results": _serialize_queryset(member_types)})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    member_type = MemberType.objects.create(**{k: v for k, v in payload.items() if k in MEMBER_TYPE_FIELDS})
    return JsonResponse(_serialize_model(member_type), status=201)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_membership_plans(request):
    if request.method == "GET":
        membership_plans = MembershipPlan.objects.all()
        return JsonResponse({"results": _serialize_queryset(membership_plans)})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    membership_plan = MembershipPlan.objects.create(**{k: v for k, v in payload.items() if k in MEMBERSHIP_PLAN_FIELDS})
    return JsonResponse(_serialize_model(membership_plan), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT"])
def api_contact(request):
    if request.method == "GET":
        contact = ContactInfo.objects.first()
        return JsonResponse(model_to_dict(contact) if contact else {})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    contact, _ = ContactInfo.objects.update_or_create(pk=1, defaults={k: v for k, v in payload.items() if k in CONTACT_FIELDS})
    return JsonResponse(model_to_dict(contact))


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_join_statements(request):
    if request.method == "GET":
        join_statements = JoinStatement.objects.all()
        return JsonResponse({"results": _serialize_queryset(join_statements)})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    join_statement = JoinStatement.objects.create(**{k: v for k, v in payload.items() if k in JOIN_STATEMENT_FIELDS})
    return JsonResponse(_serialize_model(join_statement), status=201)


@csrf_exempt
@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def api_users(request):
    if not request.user.is_staff:
        return JsonResponse({"error": "Forbidden"}, status=403)
    """List users or create a new user (simple admin API)."""
    if request.method == "GET":

        users = User.objects.all()
        qs = list(users.values('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser'))
        return JsonResponse({"results": qs})

    # POST: create user
    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    username = payload.get('username')
    email = payload.get('email')
    password = payload.get('password') or User.objects.make_random_password()
    role = (payload.get('role') or '').lower()

    if not username or not email:
        return HttpResponseBadRequest('username and email are required')

    u = User.objects.create_user(username=username, email=email, password=password)
    # simple role mapping
    if 'super' in role:
        u.is_superuser = True
        u.is_staff = True
    elif 'admin' in role:
        u.is_staff = True
    u.save()

    return JsonResponse({'id': u.id, 'username': u.username, 'email': u.email, 'is_active': u.is_active, 'is_staff': u.is_staff, 'is_superuser': u.is_superuser}, status=201)


@csrf_exempt
@login_required(login_url='login')
@require_http_methods(["GET", "PUT", "DELETE"])
def api_user_detail(request, pk):
    if not request.user.is_staff:
        return JsonResponse({"error": "Forbidden"}, status=403)
    try:
        u = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({"error": "Non trouvé"}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': u.id, 'username': u.username, 'email': u.email, 'is_active': u.is_active, 'is_staff': u.is_staff, 'is_superuser': u.is_superuser})

    if request.method == 'DELETE':
        u.delete()
        return JsonResponse({'deleted': True})

    # PUT: update
    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest('JSON invalide')

    if 'username' in payload:
        u.username = payload['username']
    if 'email' in payload:
        u.email = payload['email']
    if 'is_active' in payload:
        u.is_active = bool(payload['is_active'])
    if 'role' in payload:
        role = (payload.get('role') or '').lower()
        if 'super' in role:
            u.is_superuser = True
            u.is_staff = True
        elif 'admin' in role:
            u.is_staff = True
        else:
            u.is_staff = False
            u.is_superuser = False
    if 'password' in payload and payload['password']:
        u.set_password(payload['password'])

    u.save()
    return JsonResponse({'id': u.id, 'username': u.username, 'email': u.email, 'is_active': u.is_active, 'is_staff': u.is_staff, 'is_superuser': u.is_superuser})


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_value_detail(request, pk):
    try:
        value = Value.objects.get(pk=pk)
    except Value.DoesNotExist:
        return JsonResponse({"error": "Non trouvé"}, status=404)

    if request.method == "GET":
        return JsonResponse(_serialize_model(value))

    if request.method == "DELETE":
        value.delete()
        return JsonResponse({"deleted": True})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    _apply_updates(value, payload, VALUE_FIELDS)
    return JsonResponse(_serialize_model(value))


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_objective_detail(request, pk):
    try:
        objective = Objective.objects.get(pk=pk)
    except Objective.DoesNotExist:
        return JsonResponse({"error": "Non trouvé"}, status=404)

    if request.method == "GET":
        return JsonResponse(_serialize_model(objective))

    if request.method == "DELETE":
        objective.delete()
        return JsonResponse({"deleted": True})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    _apply_updates(objective, payload, OBJECTIVE_FIELDS)
    return JsonResponse(_serialize_model(objective))


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_action_detail(request, pk):
    try:
        action = Action.objects.get(pk=pk)
    except Action.DoesNotExist:
        return JsonResponse({"error": "Non trouvé"}, status=404)

    if request.method == "GET":
        return JsonResponse(_serialize_model(action))

    if request.method == "DELETE":
        action.delete()
        return JsonResponse({"deleted": True})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    _apply_updates(action, payload, ACTION_FIELDS)
    return JsonResponse(_serialize_model(action))


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_board_role_detail(request, pk):
    try:
        board_role = BoardRole.objects.get(pk=pk)
    except BoardRole.DoesNotExist:
        return JsonResponse({"error": "Non trouvé"}, status=404)

    if request.method == "GET":
        return JsonResponse(_serialize_model(board_role))

    if request.method == "DELETE":
        board_role.delete()
        return JsonResponse({"deleted": True})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    _apply_updates(board_role, payload, BOARD_ROLE_FIELDS)
    return JsonResponse(_serialize_model(board_role))


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_member_type_detail(request, pk):
    try:
        member_type = MemberType.objects.get(pk=pk)
    except MemberType.DoesNotExist:
        return JsonResponse({"error": "Non trouvé"}, status=404)

    if request.method == "GET":
        return JsonResponse(_serialize_model(member_type))

    if request.method == "DELETE":
        member_type.delete()
        return JsonResponse({"deleted": True})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    _apply_updates(member_type, payload, MEMBER_TYPE_FIELDS)
    return JsonResponse(_serialize_model(member_type))


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_membership_plan_detail(request, pk):
    try:
        membership_plan = MembershipPlan.objects.get(pk=pk)
    except MembershipPlan.DoesNotExist:
        return JsonResponse({"error": "Non trouvé"}, status=404)

    if request.method == "GET":
        return JsonResponse(_serialize_model(membership_plan))

    if request.method == "DELETE":
        membership_plan.delete()
        return JsonResponse({"deleted": True})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    _apply_updates(membership_plan, payload, MEMBERSHIP_PLAN_FIELDS)
    return JsonResponse(_serialize_model(membership_plan))


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_join_statement_detail(request, pk):
    try:
        join_statement = JoinStatement.objects.get(pk=pk)
    except JoinStatement.DoesNotExist:
        return JsonResponse({"error": "Non trouvé"}, status=404)

    if request.method == "GET":
        return JsonResponse(_serialize_model(join_statement))

    if request.method == "DELETE":
        join_statement.delete()
        return JsonResponse({"deleted": True})

    try:
        payload = _parse_json_body(request)
    except ValueError:
        return HttpResponseBadRequest("JSON invalide")

    _apply_updates(join_statement, payload, JOIN_STATEMENT_FIELDS)
    return JsonResponse(_serialize_model(join_statement))


@require_GET
def api_all(request):
    """Single endpoint — retourne tout le contenu du site en un appel."""
    config = _get_site_config()
    contact = ContactInfo.objects.first()

    return JsonResponse({
        "config": _serialize_config(config),
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
