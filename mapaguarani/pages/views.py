from rest_framework import viewsets
from django.contrib.sites.models import Site
from .serializers import FlatpageSerializer
from .models import Page


class FlatpageViewSet(viewsets.ReadOnlyModelViewSet):

    # model = Page
    queryset = Page.objects.all()
    serializer_class = FlatpageSerializer
    filter_fields = ('url',)

    def get_queryset(self):
        queryset = super().get_queryset()

        current_site = Site.objects.get_current()
        queryset = queryset.filter(sites=current_site)

        url_prefix = self.request.query_params.get('url_prefix')
        if url_prefix:
            queryset = queryset.filter(url__startswith=url_prefix)
        return queryset
