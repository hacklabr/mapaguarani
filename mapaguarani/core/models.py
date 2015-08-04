from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class MapLayer(models.Model):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('Description'))

    class Meta:
        verbose_name = _('Map Layer')
        verbose_name_plural = _('Map Layers')

    def __str__(self):
        return self.name


class DocumentType(models.Model):
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        verbose_name = _('Indigenous Place Document Type')
        verbose_name_plural = _('Indigenous Place Document Types')

    def __str__(self):
        return self.name


class Document(models.Model):
    name = models.CharField(_('name'), max_length=255)
    type = models.ForeignKey(DocumentType, verbose_name=_('type'))
    file = models.FileField(_('attached file'))
    # TODO verificar se a data é opcional
    date = models.DateField(_('Date'))
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('Indigenous Place Document')
        verbose_name_plural = _('Indigenous Place Documents')

    def __str__(self):
        return self.name


class EthnicGroup(models.Model):
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        verbose_name = _('Ethnic Group')
        verbose_name_plural = _('Ethnic Groups')

    def __str__(self):
        return self.name


class IndigenousPlace(models.Model):
    name = models.CharField(_('name'), max_length=255)
    other_names = models.CharField(_('Others names'), max_length=512, blank=True, null=True)
    prominent_subgroup = models.ManyToManyField(
        EthnicGroup,
        verbose_name=_('prominent ethnic sub-group'),
        related_name='%(class)s_prominent_subgroup_layers',
        blank=True
    )
    document = models.ManyToManyField(
        Document,
        verbose_name=_('documentation'),
        related_name='%(class)s_documentation',
        blank=True)
    public_comments = models.TextField(_('Comments'), blank=True, null=True)
    private_comments = models.TextField(_('Private comments'), blank=True, null=True)

    objects = models.GeoManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class IndigenousVillage(IndigenousPlace):

    POSITION_PRECISION = (
        ('exact', _('Exact')),
        ('approximate', _('Approximate')),
        ('no_info', _('No information')),
    )

    comments = models.TextField(_('Comments'), blank=True, null=True)
    ethnic_groups = models.ManyToManyField(
        EthnicGroup,
        verbose_name=_('Ethnic group'),
        related_name='%(class)s_ethnic_groups_layers',
        blank=True
    )
    position_precision = models.CharField(
        _('Land Tenure'),
        choices=POSITION_PRECISION,
        max_length=256,
        default=POSITION_PRECISION[2][0]
    )
    position_source = models.CharField(_('Source'), max_length=512)
    position = models.PointField()
    layer = models.ForeignKey(MapLayer, verbose_name=_('Layer'), related_name='villages', blank=True, null=True)

    class Meta:
        verbose_name = _('Indigenous Village')
        verbose_name_plural = _('Indigenous Villages')

    # @property
    # def population(self):
        # try:
        #     return self.anual_series_population.latest().population
        # except Population.DoesNotExist:
        #     return 0

    # @property
    # def guarani_presence(self):
        # try:
        #     return self.annual_series_guarani_presence.latest().presence
        # except GuaraniPresence.DoesNotExist:
        #     return 0

    @property
    def city(self):
        # TODO georeferential query
        pass

    @property
    def state(self):
        # TODO georeferential query
        pass

    @property
    def country(self):
        # TODO georeferential query
        pass


class GuaraniPresence(models.Model):
    presence = models.BooleanField(_('Guarani presence'))
    date = models.DateField(_('Date'))
    source = models.CharField(_('name'), max_length=512)
    village = models.ForeignKey(
        IndigenousVillage, verbose_name=_('Village'), related_name='%(class)s_annual_series_guarani_presence')

    class Meta:
        get_latest_by = 'date'
        verbose_name = _('Guarani Presence')

    def __str__(self):
        return '{}: {}'.format(self.village.name, self.presence)


class Population(models.Model):
    population = models.IntegerField(_('Population'))
    date = models.DateField(_('Date'))
    source = models.CharField(_('Source'), max_length=512)
    village = models.ForeignKey(
        IndigenousVillage, verbose_name=_('Village'), related_name='%(class)s_annual_series_population')

    class Meta:
        get_latest_by = 'date'
        verbose_name = _('Population')
        verbose_name_plural = _('Populations')

    def __str__(self):
        return '{}: {}'.format(self.village.name, self.population)


class IndigenousLand(IndigenousPlace):

    LAND_TENURE_CHOICES = (
        ('no_arrangements', _('Sem Providências')),
        ('regularized', _('Regularizada')),
        ('expropriated', _('Desapropriada')),
        ('expropriated_in_progress', _('Em processo de desapropriação')),
        ('delimited', _('Delimitada')),
        ('study', _('Em estudo')),
        ('declared', _('Declarada')),
        ('acquired', _('Adquirida')),
        ('regularized_limits_rev', _('Regularizada (Em revisão de limites)')),
    )
    LAND_TENURE_STATUS_CHOICES = (
        ('no_revision', _('No Revision')),
        ('not_delimited', _('Not Delimited')),
        ('revised_land', _('Revised Land')),
        ('original_land', _('Original Land')),
    )

    official_area = models.FloatField(_('Official area'), blank=True, null=True)
    guarani_exclusive_possession_area_portion = models.FloatField(
        _('Guarani full and exclusive portion area possession'), blank=True, null=True)
    others_exclusive_possession_area_portion = models.FloatField(
        _('Others people full and exclusive portion area possession'), blank=True, null=True)
    # private field
    claim = models.TextField(_('Clain'), blank=True, null=True)
    # private field
    demand = models.TextField(_('Demand'), blank=True, null=True)
    # private field???
    source = models.CharField(_('Source'), max_length=512)
    # Situação Fundiária
    land_tenure = models.CharField(
        _('Land Tenure'), choices=LAND_TENURE_CHOICES, max_length=256)
    # Status de revisão fundiária
    land_tenure_status = models.CharField(
        _('Land Tenure Status'), choices=LAND_TENURE_STATUS_CHOICES, max_length=256)
    associated_land = models.CharField(_('Source'), max_length=512, blank=True, null=True)
    polygon = models.MultiPolygonField(_('Indigenous Land Spatial Data'))
    layer = models.ForeignKey(MapLayer, verbose_name=_('Layer'), related_name='indigenous_lads')

    class Meta:
        verbose_name = _('Indigenous Land')
        verbose_name_plural = _('Indigenous Lands')

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
    indigenous_land = models.ForeignKey(
        IndigenousLand,
        verbose_name=_('Guarani indigenous lands layer'),
    )
    indigenous_village = models.ForeignKey(
        IndigenousVillage,
        verbose_name=_('Guarani indigenous villages layer')
    )

    class Meta:
        verbose_name = _('Legal Proceeding')
        verbose_name_plural = _('Legal Proceedings')

    def __str__(self):
        return self.name


class ArchaeologicalPlace(models.Model):
    POSITION_PRECISION_CHOICES = (
        ('exact', _('Exact')),
        ('estimated', _('Estimated')),
        ('by_city', _('By City')),
        ('no_position', _('No position')),
    )

    name = models.CharField(_('name'), max_length=255)
    acronym = models.CharField(_('name'), max_length=512)
    position_precision = models.CharField(
        _('Position Precision'),
        choices=POSITION_PRECISION_CHOICES,
        max_length=128)
    position_comments = models.TextField(_('Position Comments'))

    layer = models.ForeignKey(MapLayer, verbose_name=_('Layer'), related_name='archaeological_places')

    class Meta:
        verbose_name = _('Archaeological Place')
        verbose_name_plural = _('Archaeological Places')

    @property
    def city(self):
        # TODO georeferential query
        pass

    @property
    def state(self):
        # TODO georeferential query
        pass

    @property
    def country(self):
        # TODO georeferential query
        pass

    def __str__(self):
        return self.name
