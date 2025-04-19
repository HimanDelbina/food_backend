import django_filters
from .models import AnbarModel

class AnbarModelFilter(django_filters.FilterSet):
    class Meta:
        model = AnbarModel
        exclude = ['barcode']  # Exclude ImageField from filtering