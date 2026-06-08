from django.db import models


class SiteConfig(models.Model):
    org_name = models.CharField(max_length=200, default="Les Penseurs du Gabon")
    acronym = models.CharField(max_length=20, default="L.P.G")
    tagline = models.CharField(max_length=200, default="Pour un Gabon Meilleur")
    description = models.TextField(default="Association citoyenne de réflexion, d'action et d'amélioration du développement du Gabon")
    founded_year = models.IntegerField(default=2024)
    city = models.CharField(max_length=100, default="Libreville")
    country = models.CharField(max_length=100, default="Gabon")
    bureau_members_count = models.IntegerField(default=10)
    objectives_count = models.IntegerField(default=4)
    duration_label = models.CharField(max_length=50, default="∞")
    motto = models.CharField(max_length=200, default="Pour un Gabon Meilleur")
    motto_label = models.CharField(max_length=100, default="LA DEVISE DE L.P.G")
    logo_url = models.ImageField(upload_to="static/images/", blank=True, default="")
    cta_label = models.CharField(max_length=100, default="ENSEMBLE, BÂTISSONS L'AVENIR 🇬🇦🌍")

    class Meta:
        verbose_name = "Configuration du site"

    def __str__(self):
        return self.org_name


class Value(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    icon = models.CharField(max_length=10, default="◆")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Objective(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=10, default="◆")

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"{self.number}. {self.title}"


class Action(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=10, default="◆")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class BoardRole(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class MemberType(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10, default="◆")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class MembershipPlan(models.Model):
    PLAN_TYPES = [("simple", "Membre Simple"), ("ca", "Membre du C.A.")]
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    price = models.IntegerField()
    currency = models.CharField(max_length=10, default="FCFA")
    period = models.CharField(max_length=20, default="mois")
    title = models.CharField(max_length=100)
    subtitle = models.TextField(blank=True)
    benefits = models.JSONField(default=list)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class ContactInfo(models.Model):
    address = models.CharField(max_length=300, default="Libreville, Gabon")
    phones = models.JSONField(default=list)
    email = models.EmailField(default="lespenseursdugabon@gmail.com")
    status = models.CharField(max_length=200, default="Association à durée illimitée")

    class Meta:
        verbose_name = "Informations de contact"

    def __str__(self):
        return self.email


class JoinStatement(models.Model):
    text = models.CharField(max_length=300)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.text
