from moderation import moderation
from moderation.moderator import GenericModerator
from .models import IndigenousLand, IndigenousVillage, ArchaeologicalPlace


class BaseModerator(GenericModerator):
    auto_approve_for_staff = False
    auto_approve_for_groups = ['Administrador',]
    # subject_template_moderator
    # message_template_moderator
    # subject_template_user
    # message_template_user

moderation.register(IndigenousLand, BaseModerator)
moderation.register(IndigenousVillage, BaseModerator)
moderation.register(ArchaeologicalPlace, BaseModerator)
