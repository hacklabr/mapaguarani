from moderation import moderation
from .models import IndigenousLand, IndigenousVillage, ArchaeologicalPlace


moderation.register(IndigenousLand)
moderation.register(IndigenousVillage)
moderation.register(ArchaeologicalPlace)
