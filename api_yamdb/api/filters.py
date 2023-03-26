import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.Filter(
        field_name='genre__slug',
    )
    category = django_filters.Filter(
        field_name='category__slug',
    )

    class Meta:
        model = Title
        fields = (
            'category',
            'genre',
            'name',
            'year',
        )
