from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from core.models import IndigenousLand, ArchaeologicalPlace, IndigenousVillage
from moderation.models import ModeratedObject

from django.contrib.auth import get_user_model
User = get_user_model()


class Command(BaseCommand):
    help = 'Create moderatedObjcts for imported objects.'

    def handle(self, *args, **options):

        admin = User.objects.get(username='admin')
        def create_moderated_objects(queryset):
            contetn_type = ContentType.objects.get_for_model(queryset[0])
            for imported_object in queryset:
                moderated_obj = ModeratedObject.objects.filter(object_pk=imported_object.id,
                                             content_type=contetn_type)
                if not moderated_obj:
                    moderated_obj = ModeratedObject(object_pk=imported_object.id,
                                                    content_type=contetn_type)
                    moderated_obj.instance=imported_object
                    moderated_obj.save()
                    moderated_obj.automoderate(user=admin)

        create_moderated_objects(IndigenousLand.objects.all())
        create_moderated_objects(IndigenousVillage.objects.all())
        create_moderated_objects(ArchaeologicalPlace.objects.all())

        self.stdout.write('Objetos ModeratedObject criados com sucesso!!!')
