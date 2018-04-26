from django.utils.translation import ugettext_lazy as _
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from .models import Page


class PageForm(FlatpageForm):

    class Meta:
        model = Page
        fields = '__all__'
        widgets = {
            'content': CKEditorWidget()
        }

class PageAdmin(admin.ModelAdmin):
    """
    Page Admin
    """
    form = PageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites', 'position')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('registration_required', 'template_name'),
        }),
    )
    list_display = ('url', 'title')
    list_filter = ('sites', 'registration_required')
    search_fields = ('url', 'title')

admin.site.unregister(FlatPage)
admin.site.register(Page, PageAdmin)
