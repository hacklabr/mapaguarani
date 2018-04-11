from django.contrib.sites.models import Site

def sites(request):
    return { 'site': Site.objects.get_current() }
