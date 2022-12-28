from .models import Card
from django_filters import FilterSet

class CardListFilter(FilterSet):
    class Meta:
        model = Card
        fields = ('study_set',)
