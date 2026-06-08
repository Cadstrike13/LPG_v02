from django.core.management.base import BaseCommand
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

MOCK_CONFIG = {
    "org_name": "Les Penseurs du Gabon",
    "acronym": "L.P.G",
    "tagline": "Pour un Gabon Meilleur",
    "description": "Association citoyenne de réflexion, d'action et d'amélioration du développement du Gabon",
    "founded_year": 2024,
    "city": "Libreville",
    "country": "Gabon",
    "bureau_members_count": 10,
    "objectives_count": 4,
    "duration_label": "∞",
    "motto": "« Pour un Gabon Meilleur »",
    "motto_label": "LA DEVISE DE L.P.G",
    "logo_url": "",
    "cta_label": "ENSEMBLE, BÂTISSONS L'AVENIR 🇬🇦🌍",
}

MOCK_VALUES = [
    {
        "id": 1,
        "title": "Éducation & Savoir",
        "description": "L'éducation transforme la société gabonaise",
        "icon": "📚",
        "order": 1,
    },
    {
        "id": 2,
        "title": "Solidarité",
        "description": "Le collectif et l'entraide au cœur de nos actions",
        "icon": "🤝",
        "order": 2,
    },
    {
        "id": 3,
        "title": "Innovation",
        "description": "Solutions adaptées aux réalités locales",
        "icon": "💡",
        "order": 3,
    },
    {
        "id": 4,
        "title": "Engagement citoyen",
        "description": "Chacun a un rôle pour améliorer le pays",
        "icon": "🌍",
        "order": 4,
    },
]

MOCK_OBJECTIVES = [
    {
        "id": 1,
        "number": 1,
        "title": "Encourager l'innovation",
        "description": "Dans la gouvernance, l'éducation, la santé et le développement durable au Gabon.",
        "icon": "💡",
    },
    {
        "id": 2,
        "number": 2,
        "title": "Promouvoir l'unité nationale",
        "description": "Participation citoyenne à travers des projets communautaires visant à renforcer les liens sociaux.",
        "icon": "🇬🇦",
    },
    {
        "id": 3,
        "number": 3,
        "title": "Former & Informer",
        "description": "Rendre la jeunesse gabonaise acteur central du changement dans le pays.",
        "icon": "🎓",
    },
    {
        "id": 4,
        "number": 4,
        "title": "Projets économiques",
        "description": "Encourager la croissance locale, la création d'emplois et l'industrialisation du Gabon.",
        "icon": "📈",
    },
]

MOCK_ACTIONS = [
    {
        "id": 1,
        "title": "Forums & Débats",
        "description": "Organisation de forums de discussions et débats pour réfléchir aux solutions aux problèmes actuels du Gabon.",
        "icon": "🗣️",
        "order": 1,
    },
    {
        "id": 2,
        "title": "Développement local",
        "description": "Projets d'agriculture durable, programmes de formation technique pour les jeunes et constructions d'infrastructures.",
        "icon": "🏗️",
        "order": 2,
    },
    {
        "id": 3,
        "title": "Collaboration ONG",
        "description": "Partenariats avec des ONG locales et internationales pour renforcer l'impact de nos projets.",
        "icon": "🌐",
        "order": 3,
    },
    {
        "id": 4,
        "title": "Patrimoine culturel",
        "description": "Promotion du patrimoine gabonais à travers des événements culturels, artistiques et éducatifs.",
        "icon": "🎭",
        "order": 4,
    },
    {
        "id": 5,
        "title": "Entrepreneuriat",
        "description": "Accompagnement des porteurs de projets et soutien à l'entrepreneuriat gabonais.",
        "icon": "🚀",
        "order": 5,
    },
    {
        "id": 6,
        "title": "Gouvernance & Droit",
        "description": "Sensibilisation citoyenne et promotion de la bonne gouvernance au Gabon.",
        "icon": "⚖️",
        "order": 6,
    },
]

MOCK_BOARD_ROLES = [
    {"id": 1, "title": "Président", "order": 1},
    {"id": 2, "title": "Vice-Président", "order": 2},
    {"id": 3, "title": "Secrétaire Général", "order": 3},
    {"id": 4, "title": "Trésorier", "order": 4},
    {"id": 5, "title": "Trésorier Adjoint", "order": 5},
    {"id": 6, "title": "Communication", "order": 6},
    {"id": 7, "title": "Logistique", "order": 7},
    {"id": 8, "title": "Relations Extérieures", "order": 8},
    {"id": 9, "title": "Juridique", "order": 9},
    {"id": 10, "title": "Projets", "order": 10},
]

MOCK_MEMBER_TYPES = [
    {
        "id": 1,
        "title": "Membres Fondateurs",
        "description": "Ceux qui ont initié la création",
        "icon": "⭐",
        "order": 1,
    },
    {
        "id": 2,
        "title": "Membres Actifs",
        "description": "Adhérents qui s'acquittent de leur cotisation mensuelle",
        "icon": "✅",
        "order": 2,
    },
    {
        "id": 3,
        "title": "Membres Bienfaiteurs",
        "description": "Soutien financier ou matériel significatif",
        "icon": "💎",
        "order": 3,
    },
    {
        "id": 4,
        "title": "Membres d'Honneur",
        "description": "Personnalités reconnues pour leur engagement",
        "icon": "🏆",
        "order": 4,
    },
]

MOCK_MEMBERSHIP_PLANS = [
    {
        "id": 1,
        "plan_type": "simple",
        "price": 2000,
        "currency": "FCFA",
        "period": "mois",
        "title": "MEMBRE SIMPLE",
        "subtitle": "Tout citoyen gabonais souhaitant s'impliquer activement dans le progrès du Gabon.",
        "benefits": [
            "Accès aux forums et débats",
            "Participation aux projets",
            "Réseau citoyen engagé",
        ],
        "is_featured": False,
        "order": 1,
    },
    {
        "id": 2,
        "plan_type": "ca",
        "price": 10000,
        "currency": "FCFA",
        "period": "mois",
        "title": "MEMBRE DU C.A.",
        "subtitle": "Membres du Conseil d'Administration. Engagement renforcé au cœur de la gouvernance associative.",
        "benefits": [
            "Tous droits membre simple",
            "Vote & décisions stratégiques",
            "Responsabilités officielles",
        ],
        "is_featured": True,
        "order": 2,
    },
]

MOCK_CONTACT = {
    "address": "Libreville, Gabon",
    "phones": ["+(241) 066 431 225", "+(241) 077 217 917"],
    "email": "lespenseursdugabon@gmail.com",
    "status": "Association à durée illimitée",
}

MOCK_JOIN_STATEMENTS = [
    {"id": 1, "text": "Pensez grand, agissez maintenant", "order": 1},
    {"id": 2, "text": "Bâtissons ensemble un Gabon meilleur", "order": 2},
    {"id": 3, "text": "Rejoignez citoyens, jeunes, entrepreneurs", "order": 3},
    {"id": 4, "text": "Soyez acteur du changement, dès aujourd'hui", "order": 4},
]


class Command(BaseCommand):
    help = "Seed initial data for LPG"

    def handle(self, *args, **options):

        SiteConfig.objects.update_or_create(
            pk=1,
            defaults=MOCK_CONFIG,
        )
        self.stdout.write(self.style.SUCCESS("✅ SiteConfig chargé"))

        for item in MOCK_VALUES:
            Value.objects.update_or_create(
                pk=item["id"],
                defaults=item,
            )
        self.stdout.write(self.style.SUCCESS("✅ Values chargées"))

        for item in MOCK_OBJECTIVES:
            Objective.objects.update_or_create(
                pk=item["id"],
                defaults=item,
            )
        self.stdout.write(self.style.SUCCESS("✅ Objectives chargés"))

        for item in MOCK_ACTIONS:
            Action.objects.update_or_create(
                pk=item["id"],
                defaults=item,
            )
        self.stdout.write(self.style.SUCCESS("✅ Actions chargées"))

        for item in MOCK_BOARD_ROLES:
            BoardRole.objects.update_or_create(
                pk=item["id"],
                defaults=item,
            )
        self.stdout.write(self.style.SUCCESS("✅ BoardRoles chargés"))

        for item in MOCK_MEMBER_TYPES:
            MemberType.objects.update_or_create(
                pk=item["id"],
                defaults=item,
            )
        self.stdout.write(self.style.SUCCESS("✅ MemberTypes chargés"))

        for item in MOCK_MEMBERSHIP_PLANS:
            MembershipPlan.objects.update_or_create(
                pk=item["id"],
                defaults=item,
            )
        self.stdout.write(self.style.SUCCESS("✅ MembershipPlans chargés"))

        ContactInfo.objects.update_or_create(
            pk=1,
            defaults=MOCK_CONTACT,
        )
        self.stdout.write(self.style.SUCCESS("✅ ContactInfo chargé"))

        for item in MOCK_JOIN_STATEMENTS:
            JoinStatement.objects.update_or_create(
                pk=item["id"],
                defaults=item,
            )
        self.stdout.write(self.style.SUCCESS("✅ JoinStatements chargés"))

        self.stdout.write(
            self.style.SUCCESS(
                "🎉 Base de données LPG initialisée avec succès !"
            )
        )