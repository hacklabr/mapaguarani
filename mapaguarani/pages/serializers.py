from rest_framework import serializers
from .models import Page


class FlatpageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['id', 'url', 'title', 'content', 'position',]
