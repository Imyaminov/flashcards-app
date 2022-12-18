from pprint import pprint
import random
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.messages.views import (
    SuccessMessageMixin,
)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from .models import Card, StudySet, Folder
from .forms import CardCheckForm

# Create your views here.

class CardListView(LoginRequiredMixin, ListView):
    model = Card
    context_object_name = 'card_list'

    def get_context_data(self, **kwargs):
        context = super(CardListView, self).get_context_data()
        context['study_set'] = StudySet.objects.all().filter(author=self.request.user)
        context['folders'] = Folder.objects.all().filter(author=self.request.user)
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Card.objects.all().filter(
            is_archive=False,
            study_set__author=user,
        ).order_by('box', 'created_at')
        return queryset

class BoxView(CardListView):
    template_name = 'cards/box.html'
    form_class = CardCheckForm

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(
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


class CardCreateView(SuccessMessageMixin, CreateView):
    model = Card
    fields = ('question', 'answer', 'study_set', 'box')
    success_url = reverse_lazy('card-create')
    success_message = "The card is created successfully!"

    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['study_set'].limit_choices_to = {'author': self.request.user}
        return modelform

class CardUpdateView(CardCreateView, UpdateView):
    success_url = reverse_lazy('card-list')
    success_message = "The card is updated successfully!"

class CardDeleteView(DeleteView):
    model = Card
    template_name = 'cards/studyset_detail.html'

    def get_success_url(self):
        set = StudySet.objects.get(studyset=self.kwargs['pk'])
        return reverse('studyset-detail', kwargs={'pk': set.id})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

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

# class StudySetListView(ListView):
#     model = StudySet
#     context_object_name = 'study_set'
#     template_name = 'cards/card_list.html'
#
#     def get_queryset(self):
#         set = StudySet.objects.all().filter(author=self.request.user)
#         return set

class StudySetDetailView(DetailView):
    model = StudySet
    context_object_name = 'studyset_detail'
    template_name = 'cards/studyset_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StudySetDetailView, self).get_context_data()
        context['studyset_cards'] = StudySet.studyset_cards(context['object'])
        return context

class StudySetCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = StudySet
    fields = ('title', 'description', 'folder')
    success_url = reverse_lazy('card-list')
    success_message = ('New Study Set created successfully!')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class StudySetUpdateView(StudySetCreateView, UpdateView):
    success_message = 'Study set updated succesfully!'

    def get_success_url(self):
        return reverse('studyset-detail', kwargs={'pk': self.kwargs['pk']})

# class FolderListView(ListView):
#     model = Folder
#     context_object_name = 'folders'
#     template_name = 'cards/card_list.html'
#
#     def get_queryset(self):
#         set = Folder.objects.all().filter(author=self.request.user)
#         return set

class FolderDetailView(DetailView):
    model = Folder
    context_object_name = 'folder_detail'
    template_name = 'cards/folder_detail.html'

    def get_context_data(self, **kwargs):
        context = super(FolderDetailView, self).get_context_data()
        context['folder_studysets'] = StudySet.objects.all().filter(folder=self.kwargs['pk'])
        return context

class FolderCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Folder
    fields = ('title', 'description')
    success_url = reverse_lazy('card-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# returns user's all studysets which has no folder
def FolderNoneSetList(request, folder):
    folder_none_sets = StudySet.objects.all().filter(folder=None)
    context = {
        'sets': folder_none_sets,
        'folder': folder,
    }
    return render(request, 'cards/folder_addset.html', context)

def FolderSetRemove(self, pk):
    set = StudySet.objects.all().get(pk=pk)
    folder = set.folder.pk
    set.folder = None
    set.save()
    return redirect('folder-detail', pk=folder)

def FolderSetAdd(self, folder_id, set_id):
    set = StudySet.objects.get(pk=set_id)
    set.folder = Folder.objects.get(pk=folder_id)
    set.save()
    return redirect('folder-none-set', folder=folder_id)

def get_user(self, request):
    return self.request.user



