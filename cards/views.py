from django.shortcuts import render
from django.views.generic import (
    ListView,
)
from .models import Card

# Create your views here.

class CardListView(ListView):
    model = Card
    queryset = Card.objects.all().order_by('-box', 'created_at')
