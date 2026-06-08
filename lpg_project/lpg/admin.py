from django.contrib import admin
from .models import SiteConfig
# Register your models here.
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('org_name', 'acronym', 'founded_year', 'city', 'country', 'logo_url')
    search_fields = ('org_name', 'acronym', 'city', 'country')
    fieldsets = (
        (None, {
            'fields': ('org_name', 'acronym', 'tagline', 'description', 'founded_year', 'city', 'country', 'logo_url')
        }),
        ('Affichage', {
            'fields': ('bureau_members_count', 'objectives_count', 'duration_label', 'motto', 'motto_label', 'cta_label')
        }),
    )
admin.site.register(SiteConfig, SiteConfigAdmin)