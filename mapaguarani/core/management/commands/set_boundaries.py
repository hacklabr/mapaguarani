from django.core.management.base import BaseCommand
from boundaries.models import City, State, Country
from core.models import IndigenousLand, ArchaeologicalPlace, IndigenousVillage


class Command(BaseCommand):
    help = 'Set Cities, States and Country for Villages, Lands and ArchaeologicalPlaces'

    def set_place_boundaries(self, queryset):

        for instance in queryset.iterator():
            instance.cities = City.objects.filter(geometry__covers=instance.geometry)
            instance.states = State.objects.filter(geometry__covers=instance.geometry)
            try:
                instance.country = Country.objects.get(geometry__covers=instance.geometry)
            except Country.DoesNotExist:
                self.stdout.write('Place {0} is not in any country!!!'.format(instance.name))
            instance.save()

    def handle(self, *args, **options):

        self.stdout.write('Starting set villages...')
        self.set_place_boundaries(IndigenousVillage.objects.all())
        self.stdout.write('Finished set villages!')
        self.stdout.write('Starting set Archaeological...')
        self.set_place_boundaries(ArchaeologicalPlace.objects.all())
        self.stdout.write('Finished set Archaeological!')

        self.stdout.write('Starting set lands...')
        for land in IndigenousLand.objects.all().iterator():
            land.cities = City.objects.filter(geometry__intersects=land.geometry)
            land.states = State.objects.filter(geometry__intersects=land.geometry)
            try:
                 land.country = Country.objects.get(geometry__covers=land.geometry)
            except Country.DoesNotExist:
                self.stdout.write('Land {0} is not in any counry!!!'.format(land.name))
            land.save()
        self.stdout.write('Finished set lands!')

        self.stdout.write('\n')
        self.stdout.write(
            'Cities, States and Country for Villages, Lands and ArchaeologicalPlaces succesfull set!!!')
        self.stdout.write('\n')
