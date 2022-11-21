from pprint import pprint
import random
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)
from django.contrib.messages.views import (
    SuccessMessageMixin,
)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Card
from .forms import CardCheckForm

# Create your views here.

class CardListView(ListView):
    model = Card
    queryset = Card.objects.all().filter(is_archive=False).order_by('box', 'created_at')

class BoxView(CardListView):
    template_name = 'cards/box.html'
    form_class = CardCheckForm

    def get_queryset(self):
        return super().queryset.filter(
            box=self.kwargs['box_num'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['box_number'] = self.kwargs['box_num']
        if self.object_list:
            context['check_card'] = random.choices(self.object_list)
        # pprint(type(random.choices(self.object_list)))

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            card = get_object_or_404(
                Card,
                id=form.cleaned_data['card_id'],
            )
            card.move(form.cleaned_data['solved'])

        return redirect(request.META.get('HTTP_REFERER'))


class CardCreateView(SuccessMessageMixin, CreateView):
    model = Card
    fields = ('question', 'answer', 'box')
    success_url = reverse_lazy('card-create')
    success_message = "The card is created successfully!"


class CardUpdateView(CardCreateView, UpdateView):
    success_url = reverse_lazy('card-list')
    success_message = "The card is updated successfully!"


class ArchivedCardListView(ListView):
    context_object_name = 'archived_cards'
    template_name = 'cards/archived_cards.html'

    def get_queryset(self):
        return Card.objects.all().filter(is_archive=True)


def change_status(request, pk):
    # print('entered <change_status> method')
    card = get_object_or_404(Card, id=pk)
    card.archive_unarchive_card()
    if card.is_archive == True:
        return redirect('card-list')
    else:
        return redirect('archived-cards')


