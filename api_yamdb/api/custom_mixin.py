from rest_framework import mixins, viewsets


class CustomMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """ Миксин, позволяющий соблюдать DRY в файле views.py."""
