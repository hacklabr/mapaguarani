from django.db import models
from django.utils.translation import ugettext_lazy as _


class DocumentationType(models.Model):
    name = models.CharField(_('name'), max_length=255)


class Documentation(models.Model):
    type = models.ForeignKey(DocumentationType, verbose_name=_('type'))
    file = models.FileField(_('attached file'))
    # verificar se a data é opcional
    date = models.DateField(_('Date'))
    description = models.TextField(_('description'), blank=True, null=True)


class EthnicGroup(models.Model):
    name = models.CharField(_('name'), max_length=255)


class IndigenousLayer(models.Model):
    name = models.CharField(_('name'), max_length=255)
    other_names = models.CharField(_('name'), max_length=512)
    ethnic_groups = models.ManyToManyField(
        EthnicGroup,
        verbose_name=_('ethnic group'),
        related_name='%(class)s_ethnic_groups_layers'
    )
    prominent_subgroup = models.ManyToManyField(
        EthnicGroup,
        verbose_name=_('prominent ethnic sub-group'),
        related_name='%(class)s_prominent_subgroup_layers'
    )
    documentation = models.ManyToManyField(Documentation, verbose_name=_('documentation'))

    class Meta:
        abstract = True


class VillagesLayer(IndigenousLayer):
    comments = models.TextField(_('Comments'), blank=True, null=True)

    @property
    def population(self):
        # try:
        #     return self.anual_series_population.latest().population
        # except Population.DoesNotExist:
        #     return 0
        pass

    @property
    def guarani_presence(self):
        # try:
        #     return self.annual_series_guarani_presence.latest().presence
        # except GuaraniPresence.DoesNotExist:
        #     return 0
        pass

    @property
    def city(self):
        # TODO georeferential query
        pass

    @property
    def state(self):
        # TODO georeferential query
        pass

    @property
    def cowntry(self):
        # TODO georeferential query
        pass


class GuaraniPresence(models.Model):
    presence = models.BooleanField(_('Guarani presence'))
    date = models.DateField(_('Date'))
    source = models.CharField(_('name'), max_length=512)
    village = models.ForeignKey(
        VillagesLayer,
        verbose_name=_('Village'),
        # related_name='%(class)s_annual_series_guarani_presence'
    )

    class Meta:
        get_latest_by = 'date'


class Population(models.Model):
    population = models.IntegerField(_('Population'))
    date = models.DateField(_('Date'))
    source = models.CharField(_('name'), max_length=512)
    village = models.ForeignKey(
        VillagesLayer,
        verbose_name=_('Village'),
        related_name='%(class)s_annual_series_population'
    )

    class Meta:
        get_latest_by = 'date'


class LandsLayer(IndigenousLayer):
    official_area = models.FloatField(_(''))
    guarani_exclusive_possession_area_portion = models.FloatField(
        _('Guarani full and exclusive portion area possession'),
        blank=True,
        null=True
    )
    others_exclusive_possession_area_portion = models.FloatField(
        _('Others people full and exclusive portion area possession'),
        blank=True,
        null=True
    )
    # private field
    claim = models.TextField(_('Clain'), blank=True, null=True)
    # private field
    demand = models.TextField(_('Demand'), blank=True, null=True)
    # private field???
    source = models.CharField(_('name'), max_length=512)


    @property
    def villages(self):
        # TODO georeferential query VillageLayer
        pass

    @property
    def population(self):
        # TODO georeferential query VillageLayer: summ of villages populations
        pass

    @property
    def calculated_area(self):
        # TODO shape field calc: only make sense depending on Land situacion
        pass


class LegalProceedings(models.Model):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('Description'))
    indigenous_land_layer = models.ForeignKey(
        LandsLayer,
        verbose_name=_('Guarani indigenous lands layer'),
    )
    indigenous_village_layer = models.ForeignKey(
        VillagesLayer,
        verbose_name=_('Guarani indigenous villages layer')
    )
