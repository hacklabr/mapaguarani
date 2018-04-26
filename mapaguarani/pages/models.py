from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _


class Page(FlatPage):
    position = models.IntegerField(_('Position'), default=0, null=True, blank=True)
