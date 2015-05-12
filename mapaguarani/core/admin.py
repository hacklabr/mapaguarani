from django.contrib import admin
from .models import (
    IndigenousVillage, IndigenousLand, LegalProceedings, DocumentationType,
    Documentation, EthnicGroup, GuaraniPresence, Population,
    ArchaeologicalPlace,
)


@admin.register(IndigenousVillage)
class IndigenousVillageAdmin(admin.ModelAdmin):
    pass


@admin.register(IndigenousLand)
class IndigenousLandAdmin(admin.ModelAdmin):
    pass


@admin.register(LegalProceedings)
class LegalProceedingsAdmin(admin.ModelAdmin):
    pass


@admin.register(ArchaeologicalPlace)
class ArchaeologicalPlaceAdmin(admin.ModelAdmin):
    pass


admin.site.register(DocumentationType)
admin.site.register(Documentation)
admin.site.register(EthnicGroup)
admin.site.register(GuaraniPresence)
admin.site.register(Population)
