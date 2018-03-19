from django.contrib.gis.db import models
from django.contrib.gis.db.models import Max, Sum
from django.utils.translation import ugettext_lazy as _
from protected_areas.models import BaseProtectedArea
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError

from boundaries.models import City, State, Country


class Organization(models.Model):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    address = models.CharField(_('address'), max_length=512, blank=False, null=True)
    phone = models.CharField(_('phone number'), max_length=255, blank=False, null=True)
    email = models.EmailField(_('email'), blank=False, null=True)

    def __str__(self):
        return self.name

class MapLayer(models.Model):

    STATUS = (
        ('public', _('Public')),
        ('restricted', _('Restricted')),
    )

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('Description'), blank=True, null=True)
    sites = models.ManyToManyField(Site)
    status = models.CharField(
        _('Status'),
        choices=STATUS,
        max_length=256,
        default=STATUS[1][0]
    )

    class Meta:
        verbose_name = _('Map Layer')
        verbose_name_plural = _('Map Layers')

    def __str__(self):
        return self.name


class ActionField(models.Model):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    layers = models.ManyToManyField(
        MapLayer,
        verbose_name=_('Layers'),
        related_name='action_fields',
        blank=True
    )

    organizations = models.ManyToManyField(
        Organization,
        verbose_name=_('Organization'),
        related_name='action_fields',
        blank=True
    )
    projects = models.ManyToManyField(
        'Project',
        verbose_name=_('Project'),
        related_name='action_fields',
        blank=True
    )

    def __str__(self):
        return self.name

class ProjectFile(models.Model):

    TYPE = (
        ('photo', _('Photo')),
        ('video', _('Video')),
        ('audio', _('Audio')),
        ('pdf', _('PDF')),
        ('others', _('Others')),
    )
    name = models.CharField(_('Name'), max_length=255, blank=True, null=True)
    desc = models.TextField(_('Description'), blank=True, null=True)
    credits = models.CharField(_('Credits (for photos)'), max_length=512, blank=True, null=True)
    type = models.CharField(
        _('Type'),
        choices=TYPE,
        max_length=256,
        default=TYPE[1][0]
    )
    file = models.FileField(_('File'))

    def __str__(self):
        return self.name

class ProjectLink(models.Model):

    TYPE = (
        ('youtube', _('youtube')),
        ('vimeo', _('vimeo')),
        ('flickr', _('flickr')),
        ('instagram', _('instagram')),
        ('others', _('Others')),
    )
    name = models.CharField(_('Name'), max_length=255, blank=True, null=True)
    desc = models.TextField(_('Description'), blank=True, null=True)
    url = models.CharField(_('Link'), max_length=512)
    embed_code = models.TextField(_('Embed code'), blank=True, null=True)
    type = models.CharField(
        _('Type'),
        choices=TYPE,
        max_length=256,
        default=TYPE[1][0]
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    start_date = models.DateField(_('start date'), blank=True, null=True)
    end_date = models.DateField(_('end date'), blank=True, null=True)
    files = models.ManyToManyField(
        'ProjectFile',
        verbose_name=_('Files'),
        related_name='files',
        blank=True
    )
    links = models.ManyToManyField(
        'ProjectLink',
        verbose_name=_('Links (Youtube, instagram, etc)'),
        related_name='links',
        blank=True
    )
    indigenous_villages = models.ManyToManyField(
        'IndigenousVillage',
        verbose_name=_('Indigenous Village'),
        related_name='projects',
        blank=True
    )
    indigenous_lands = models.ManyToManyField(
        'IndigenousLand',
        verbose_name=_('Indigenous Land'),
        related_name='projects',
        blank=True
    )
    archaeological_places = models.ManyToManyField(
        'ArchaeologicalPlace',
        verbose_name=_('Archaeological Place'),
        related_name='projects',
        blank=True
    )
    organizations = models.ManyToManyField(
        Organization,
        verbose_name=_('Organization'),
        related_name='projects',
        blank=True
    )
    layers = models.ManyToManyField(
        MapLayer,
        verbose_name=_('Layers'),
        related_name='projects',
        blank=True
    )


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

    STATUS = (
        ('public', _('Public')),
        ('restricted', _('Restricted')),
    )

    name = models.CharField(_('name'), max_length=255)
    other_names = models.CharField(_('Others names'), max_length=512, blank=True, null=True)
    ethnic_groups = models.ManyToManyField(
        EthnicGroup,
        verbose_name=_('Ethnic group'),
        related_name='%(class)s_ethnic_groups_layers'
    )
    prominent_subgroup = models.ManyToManyField(
        ProminentEthnicSubGroup,
        verbose_name=_('prominent ethnic sub-group'),
        related_name='%(class)s_prominent_subgroup_layers',
        blank=True
    )
    public_comments = models.TextField(_('Comments'), blank=True, null=True)
    private_comments = models.TextField(_('Private comments'), blank=True, null=True)
    status = models.CharField(
        _('Status'),
        choices=STATUS,
        max_length=256,
        default=STATUS[1][0]
    )

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
    layer = models.ForeignKey(MapLayer, verbose_name=_('Layer'), related_name='villages')

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
        try:
            return City.objects.get(geometry__covers=self.geometry)
        except City.DoesNotExist:
            return

    @property
    def state(self):
        try:
            return State.objects.get(geometry__covers=self.geometry)
        except State.DoesNotExist:
            return

    @property
    def country(self):
        try:
            return Country.objects.get(geometry__covers=self.geometry)
        except Country.DoesNotExist:
            return
        except Country.MultipleObjectsReturned:
            # import ipdb;ipdb.set_trace()
            return


class GuaraniPresence(models.Model):
    '''
    We have been asked to rename all Guarani Presence fields to Indigenous Presence.
    So, changed on the presentation - the backend stays the same
    '''
    presence = models.BooleanField(_('Indigenous Presence'))
    date = models.DateField(_('Date'))
    source = models.CharField(_('Source'), max_length=512)
    village = models.ForeignKey(
        IndigenousVillage, verbose_name=_('Village'), related_name='guarani_presence_annual_series')

    class Meta:
        get_latest_by = 'date'
        verbose_name = _('Indigenous Presence')

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
    dashed_border = models.BooleanField(_('Dashed border'), default=False)

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
        _("Other peoples' full and exclusive portion area possession"), blank=True, null=True)
    # private field
    claim = models.TextField(_('Claim'), blank=True, null=True)
    # private field
    demand = models.TextField(_('Demand'), blank=True, null=True)

    source = models.CharField(_('Source'), max_length=512)
    # Situação Fundiária
    land_tenure = models.ForeignKey(
        LandTenure,
        verbose_name=_('Land Tenure'),
        related_name='indigenous_lands') #,
        # blank=True, null=True)
    # Status de revisão fundiária
    land_tenure_status = models.ForeignKey(
        LandTenureStatus,
        verbose_name=_('Land Tenure Status'),
        related_name='indigenous_lands') #,
        # blank=True, null=True)
    associated_land = models.ForeignKey(
        'self',
        verbose_name=_('Associated Land'),
        blank=True, null=True)
    geometry = models.MultiPolygonField(_('Indigenous Land Spatial Data'))
    layer = models.ForeignKey(MapLayer, verbose_name=_('Layer'), related_name='indigenous_lads')  # TODO: fix typo

    class Meta:
        verbose_name = _('Indigenous Land')
        verbose_name_plural = _('Indigenous Lands')

    def clean(self):
        if self.associated_land:
            if not self.land_tenure_status:
                raise ValidationError('associated_land without land_tenure_status')
            if self.land_tenure_status.name != 'Terra Original' or self.land_tenure_status.name != "Terra Revisada":
                raise ValidationError('land_tenure_status is not "Terra Original" nor "Terra Revisada"')

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

    @property
    def country(self):
        try:
            return Country.objects.get(geometry__covers=self.geometry)
        except Country.DoesNotExist:
            return
        except Country.MultipleObjectsReturned:
            # countries = Country.objects.filter(geometry__covers=self.geometry)
            # import ipdb;ipdb.set_trace()
            return

class LegalProcedings(models.Model):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('Description'))
    indigenous_land = models.ManyToManyField(
        IndigenousLand,
        verbose_name=_('Guarani indigenous lands layer'),
    )
    indigenous_village = models.ManyToManyField(
        IndigenousVillage,
        verbose_name=_('Guarani indigenous villages layer')
    )

    class Meta:
        verbose_name = _('Legal Proceding')
        verbose_name_plural = _('Legal Procedings')

    def __str__(self):
        return self.name


class ArchaeologicalPlace(models.Model):
    POSITION_PRECISION_CHOICES = (
        ('exact', _('Exact')),
        ('approximate', _('Approximate')),
        ('by_city', _('By City')),
        ('no_position', _('No position')),
    )

    STATUS = (
        ('public', _('Public')),
        ('restricted', _('Restricted')),
    )

    name = models.CharField(_('name'), max_length=255)
    acronym = models.CharField(_('Acronym'), max_length=512, blank=True, null=True)
    cnsa = models.CharField(_('CNSA'), max_length=512, blank=True, null=True)
    position_precision = models.CharField(
        _('Position Precision'),
        choices=POSITION_PRECISION_CHOICES,
        max_length=128)
    position_comments = models.TextField(_('Position Comments'))
    biblio_references = models.CharField(_('Source'), max_length=512, blank=True, null=True)

    status = models.CharField(
        _('Status'),
        choices=STATUS,
        max_length=256,
        default=STATUS[1][0]
    )
    institution = models.CharField(_('institution'), max_length=512, blank=True, null=True)
    hydrography = models.CharField(_('hydrography'), max_length=512, blank=True, null=True)
    phase = models.CharField(_('phase'), max_length=255, blank=True, null=True)
    dating = models.CharField(_('dating'), max_length=255, blank=True, null=True)
    deviation = models.CharField(_('deviation'), max_length=255, blank=True, null=True)
    chrono_ref = models.CharField(_('chronological reference'), max_length=255, blank=True, null=True)
    ap_date = models.CharField(_('ap date'), max_length=255, blank=True, null=True)
    calibrated_dating = models.CharField(_('calibrated dating'), max_length=255, blank=True, null=True)
    dating_method = models.CharField(_('dating method'), max_length=255, blank=True, null=True)
    lab_code = models.CharField(_('laboratory code'), max_length=255, blank=True, null=True)

    layer = models.ForeignKey(MapLayer, verbose_name=_('Layer'), related_name='archaeological_places')
    geometry = models.PointField()

    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Archaeological Place')
        verbose_name_plural = _('Archaeological Places')

    @property
    def protected_areas(self):
        return BaseProtectedArea.objects.filter(geometry__covers=self.geometry)

    @property
    def city(self):
        try:
            return City.objects.get(geometry__covers=self.geometry)
        except City.DoesNotExist:
            return

    @property
    def state(self):
        try:
            return State.objects.get(geometry__covers=self.geometry)
        except State.DoesNotExist:
            return

    @property
    def country(self):
        try:
            return Country.objects.get(geometry__covers=self.geometry)
        except Country.DoesNotExist:
            return
        except Country.MultipleObjectsReturned:
            # countries = Country.objects.filter(geometry__covers=self.geometry)
            # import ipdb;ipdb.set_trace()
            return

    @property
    def land(self):
        return IndigenousLand.objects.filter(geometry__covers=self.geometry)

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


