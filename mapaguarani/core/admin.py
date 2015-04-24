from django.contrib import admin
from .models import (
    VillagesLayer, LandsLayer, LegalProceedings, DocumentationType,
    Documentation, EthnicGroup, GuaraniPresence, Population,
)


@admin.register(VillagesLayer)
class VillagesLayerAdmin(admin.ModelAdmin):
    pass

@admin.register(LandsLayer)
class LandsLayerAdmin(admin.ModelAdmin):
    pass

@admin.register(LegalProceedings)
class LegalProceedingsAdmin(admin.ModelAdmin):
    pass


admin.site.register(DocumentationType)
admin.site.register(Documentation)
admin.site.register(EthnicGroup)
admin.site.register(GuaraniPresence)
admin.site.register(Population)
