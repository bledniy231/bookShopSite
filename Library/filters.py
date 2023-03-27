import django_filters
from .models import Books


class ListingFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    author = django_filters.CharFilter(field_name="author", lookup_expr="icontains")

    class Meta:
        model = Books
        fields = ['name', 'author']