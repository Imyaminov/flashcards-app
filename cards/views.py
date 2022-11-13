from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)
from django.urls import reverse_lazy
from .models import Card

# Create your views here.

class CardListView(ListView):
    model = Card
    queryset = Card.objects.all().order_by('box', 'created_at')

class BoxView(CardListView):
    template_name = 'cards/box.html'
    context_object_name = 'box_cards'

    def get_queryset(self):
        return Card.objects.all.filter(box=self.kwargs['bux_num'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BoxView, self).get_context_data(**kwargs)
        context['box_number'] = self.kwargs['box_num']
        return context

class CardCreateView(CreateView):
    model = Card
    fields = ('question', 'answer', 'box')
    success_url = reverse_lazy('card-create')

class CardUpdateView(CardCreateView, UpdateView):
    # context_object_name = 'card_u'
    success_url = reverse_lazy('card-list')



