import django_filters
from django_filters import DateFilter, CharFilter
from .models import *


class ContentFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name='updated', lookup_expr='gte')
    # end_date = DateFilter(field_name='updated', lookup_expr='lte')
    note = CharFilter(field_name='month_name', lookup_expr='icontains')
    class Meta:
        model = Content
        fields = '__all__'
        exclude = ['title', 'month_name', 'monthly_active_user', 'global_rank', 'country_traffic', 'social_media_traffic', 'updated']


class BrandFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    language = CharFilter(field_name='language', lookup_expr='icontains')
    website = CharFilter(field_name='website', lookup_expr='icontains')
    # start_date = DateFilter(field_name='created', lookup_expr='gte')
    # end_date = DateFilter(field_name='created', lookup_expr='lte')

    class Meta:
        model = Brand
        fields = '__all__'
        exclude = ['slug', 'title', 'website', 'language', 'created']