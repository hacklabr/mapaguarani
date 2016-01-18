from django.contrib.gis.db import models
from django.contrib.gis.db.models import Max, Sum
from django.contrib.gis.db.models.aggregates import Collect
from django.utils.translation import ugettext_lazy as _
from protected_areas.models import BaseProtectedArea

from boundaries.models import City, State


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


class ProminentEthnicSubGroup(models.Model):
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        verbose_name = _('Prominent Ethnic SubGroup')
        verbose_name_plural = _('Prominent Ethnic SubGroups')

    def __str__(self):
        return self.name


class IndigenousPlace(models.Model):
    name = models.CharField(_('name'), max_length=255)
    other_names = models.CharField(_('Others names'), max_length=512, blank=True, null=True)
    ethnic_groups = models.ManyToManyField(
        EthnicGroup,
        verbose_name=_('Ethnic group'),
        related_name='%(class)s_ethnic_groups_layers',
        blank=True
    )
    prominent_subgroup = models.ManyToManyField(
        ProminentEthnicSubGroup,
        verbose_name=_('prominent ethnic sub-group'),
        related_name='%(class)s_prominent_subgroup_layers',
        blank=True
    )
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

    position_precision = models.CharField(
        _('Position Precision'),
        choices=POSITION_PRECISION,
        max_length=256,
        default=POSITION_PRECISION[2][0]
    )
    position_source = models.CharField(_('Position Source'), max_length=512)
    geometry = models.PointField()
    layer = models.ForeignKey(MapLayer, verbose_name=_('Layer'), related_name='villages', blank=True, null=True)

    class Meta:
        verbose_name = _('Indigenous Village')
        verbose_name_plural = _('Indigenous Villages')

    @property
    def population(self):
        try:
            return self.population_annual_series.latest().population
        except Population.DoesNotExist:
            return 0

    @property
    def guarani_presence(self):
        try:
            return self.guarani_presence_annual_series.latest().presence
        except GuaraniPresence.DoesNotExist:
            return False

    @property
    def land(self):
        return IndigenousLand.objects.filter(geometry__covers=self.geometry)

    @property
    def protected_areas(self):
        return BaseProtectedArea.objects.filter(geometry__covers=self.geometry)

    @property
    def city(self):
        return City.objects.get(geometry__covers=self.geometry)

    @property
    def state(self):
        return State.objects.get(geometry__covers=self.geometry)

    @property
    def country(self):
        return 'Brasil'


class GuaraniPresence(models.Model):
    presence = models.BooleanField(_('Guarani presence'))
    date = models.DateField(_('Date'))
    source = models.CharField(_('name'), max_length=512)
    village = models.ForeignKey(
        IndigenousVillage, verbose_name=_('Village'), related_name='guarani_presence_annual_series')

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
        IndigenousVillage, verbose_name=_('Village'), related_name='population_annual_series')

    class Meta:
        get_latest_by = 'date'
        verbose_name = _('Population')
        verbose_name_plural = _('Populations History')

    def __str__(self):
        return '{}: {}'.format(self.village.name, self.population)


class LandTenure(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    map_color = models.CharField(_('Color in Map'), max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = _('Land Tenure')
        verbose_name_plural = _('Land Tenures')

    def __str__(self):
        return self.name

    def state_lands_count(self, acronym):
        state = State.objects.filter(acronym=acronym).first()
        if state:
            return self.indigenous_lands.filter(geometry__coveredby=state.geometry).count()
        return 0

    def es_lands_count(self):
        return self.state_lands_count('ES')

    def pr_lands_count(self):
        return self.state_lands_count('PR')

    def rj_lands_count(self):
        return self.state_lands_count('RJ')

    def rs_lands_count(self):
        return self.state_lands_count('RS')

    def sc_lands_count(self):
        return self.state_lands_count('SC')

    def sp_lands_count(self):
        return self.state_lands_count('SP')


class LandTenureStatus(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    map_color = models.CharField(_('Color in Map'), max_length=64, blank=True, null=True)
    dashed_border = models.BooleanField(_('Dasshed border'), default=False)

    class Meta:
        verbose_name = _('Land Tenure Status')
        verbose_name_plural = _('Land Tenures Status')

    def __str__(self):
        return self.name


class IndigenousLand(IndigenousPlace):

    documents = models.ManyToManyField(
        Document,
        verbose_name=_('documentation'),
        related_name='%(class)s_documentation',
        blank=True)
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
    land_tenure = models.ForeignKey(
        LandTenure,
        verbose_name=_('Land Tenure'),
        related_name='indigenous_lands',
        blank=True, null=True)
    # Status de revisão fundiária
    land_tenure_status = models.ForeignKey(
        LandTenureStatus,
        verbose_name=_('Land Tenure Status'),
        related_name='indigenous_lands',
        blank=True, null=True)
    associated_land = models.ForeignKey(
        'self',
        verbose_name=_('Associated Land'),
        blank=True, null=True)
    geometry = models.MultiPolygonField(_('Indigenous Land Spatial Data'))
    layer = models.ForeignKey(MapLayer, verbose_name=_('Layer'), related_name='indigenous_lads')  # TODO: fix typo

    class Meta:
        verbose_name = _('Indigenous Land')
        verbose_name_plural = _('Indigenous Lands')

    @property
    def villages(self):
        # return IndigenousVillage.objects.filter(geometry__contained=self.geometry)
        return IndigenousVillage.objects.filter(geometry__coveredby=self.geometry)

    @property
    def population(self):
        total = Population.objects.filter(village__geometry__coveredby=self.geometry)\
                                  .values('population').annotate(latest=Max('village'))\
                                  .aggregate(total_population=Sum('population'))\
                                  .get('total_population')
        return total or 0

    @property
    def calculated_area(self):
        return False
        # TODO test 29101 (http://spatialreference.org/ref/epsg/29101/)
        # return self.geometry.transform(27700, clone=True).area / 10000

    @property
    def protected_areas(self):
        return BaseProtectedArea.objects.filter(geometry__intersects=self.geometry)

    def get_cities_intersected(self):
        return City.objects.filter(geometry__intersects=self.geometry)

    def get_states_intersected(self):
        return State.objects.filter(geometry__intersects=self.geometry)


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
    code = models.CharField(_('Code'), max_length=255, blank=True, null=True)
    acronym = models.CharField(_('Acronym'), max_length=512, blank=True, null=True)
    cnsa = models.CharField(_('CNSA'), max_length=512, blank=True, null=True)
    geometry = models.PointField()
    position_precision = models.CharField(
        _('Position Precision'),
        choices=POSITION_PRECISION_CHOICES,
        max_length=128)
    position_comments = models.TextField(_('Position Comments'))
    biblio_references = models.CharField(_('Source'), max_length=512, blank=True, null=True)

    layer = models.ForeignKey(MapLayer, verbose_name=_('Layer'), related_name='archaeological_places')

    objects = models.GeoManager()

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


class ArchaeologicalImage(models.Model):
    name = models.CharField(_('name'), max_length=255, blank=True, null=True)
    desc = models.TextField(_('Description'), blank=True, null=True)
    credits = models.CharField(_('Credits'), max_length=512, blank=True, null=True)
    image = models.ImageField(_('Image'))
    archaeological_place = models.ForeignKey(
        ArchaeologicalPlace,
        verbose_name=_('Archaeological Place'),
        related_name='images')
