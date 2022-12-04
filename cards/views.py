from pprint import pprint
import random
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.messages.views import (
    SuccessMessageMixin,
)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Card, StudySet, Folder
from .forms import CardCheckForm

# Create your views here.

class CardListView(LoginRequiredMixin, ListView):
    model = Card
    queryset = Card.objects.all().filter(is_archive=False).order_by('box', 'created_at')

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(study_set__author=user)

class BoxView(CardListView):
    template_name = 'cards/box.html'
    form_class = CardCheckForm

    def get_queryset(self):
        user = self.request.user
        return super().queryset.filter(
            box=self.kwargs['box_num'],
            study_set__author=user
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


class CardCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Card
    fields = ('question', 'answer', 'study_set', 'box')
    success_url = reverse_lazy('card-create')
    success_message = "The card is created successfully!"

    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['study_set'].limit_choices_to = {'author': self.request.user}
        return modelform

class CardUpdateView(CardCreateView, LoginRequiredMixin, UpdateView):
    success_url = reverse_lazy('card-list')
    success_message = "The card is updated successfully!"


class ArchivedCardListView(ListView):
    context_object_name = 'archived_cards'
    template_name = 'cards/archived_cards.html'

    def get_queryset(self):
        user = self.request.user
        return Card.objects.all().filter(is_archive=True,study_set__author=user)

# method to archive and unarchive cards
def change_status(request, pk):
    # print('entered <change_status> method')
    card = get_object_or_404(Card, id=pk)
    card.archive_unarchive_card()
    if card.is_archive == True:
        return redirect('card-list')
    else:
        return redirect('archived-cards')

class StudySetListView(ListView):
    model = StudySet

    def get_queryset(self):
        set = StudySet.objects.all().filter(author=self.request.user)
        return set

class StudySetCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = StudySet
    fields = ('title', 'description')
    success_url = reverse_lazy('card-list')
    success_message = ('New Study Set created successfully!')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class FolderListView(ListView):
    model = Folder

    def get_queryset(self):
        set = Folder.objects.all().filter(author=self.request.user)
        return set

class FolderCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Folder
    fields = ('title', 'description')
    success_url = reverse_lazy('card-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def get_user(self, request):
    return self.Frequest.user
