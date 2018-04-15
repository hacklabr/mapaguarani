from moderation import moderation
from moderation.moderator import GenericModerator

from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from .models import IndigenousLand, IndigenousVillage, ArchaeologicalPlace


class BaseModerator(GenericModerator):
    auto_approve_for_staff = False
    auto_approve_for_groups = ['Administrador',]
    # subject_template_moderator
    # message_template_moderator
    # subject_template_user
    # message_template_user
    # Use these lines to run fix_moderation_after_imports
    notify_moderator = False
    notify_user = False

    def send(self, content_object, subject_template, message_template,
             recipient_list, extra_context=None):
        # FIXME: when rejecting, the content_object is None. This seens to be a BUG in moderator.models
        if not content_object:
            return
        context = {
            'moderated_object': content_object.moderated_object,
            'content_object': content_object,
            'site': Site.objects.get_current(),
            'content_type': content_object.moderated_object.content_type}
        if extra_context:
            context.update(extra_context)

        message = render_to_string(message_template, context)
        subject = render_to_string(subject_template, context)

        backend = self.get_message_backend()
        backend.send(
            subject=subject,
            message=message,
            recipient_list=recipient_list)
moderation.register(IndigenousLand, BaseModerator)
moderation.register(IndigenousVillage, BaseModerator)
moderation.register(ArchaeologicalPlace, BaseModerator)
