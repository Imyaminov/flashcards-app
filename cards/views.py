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
from .filters import CardListFilter
class CardListView(LoginRequiredMixin, ListView):
    model = Card
    context_object_name = 'card_list'
    filter_set = CardListFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Card.objects.all().filter(
            is_archive=False,
            study_set__author=user,
        ).order_by('box', 'created_at')
        card_filter = CardListFilter(self.request.GET, queryset=queryset)
        return card_filter.qs

    def get_context_data(self, **kwargs):
        context = super(CardListView, self).get_context_data()
        context['study_set'] = StudySet.objects.all().filter(author=self.request.user)
        context['folders'] = Folder.objects.all().filter(author=self.request.user)

        queryset = self.get_queryset()
        filter = CardListFilter(self.request.GET, queryset)
        context["filter"] = filter
        return context

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


class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    fields = ('question', 'answer', 'box')

    # def get_form_class(self):
    #     modelform = super().get_form_class()
    #     modelform.base_fields['study_set'].limit_choices_to = {'author': self.request.user}
    #     return modelform

    def get_context_data(self, **kwargs):
        context = super(CardCreateView, self).get_context_data()
        context['set_id'] = self.kwargs['set']
        return context

    def form_valid(self, form, *args):
        form.instance.study_set = StudySet.objects.get(pk=self.kwargs['set'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('card-create', kwargs={'set': self.kwargs['set']})

class CardUpdateView(UpdateView):
    model = Card
    fields = ('question', 'answer')
    template_name = 'cards/card_form.html'

    def get_context_data(self, **kwargs):
        context = super(CardUpdateView, self).get_context_data()
        card_set_id = StudySet.objects.get(studyset=self.kwargs['pk'])
        context['set_id'] = card_set_id.id
        return context

    def get_success_url(self):
        return reverse('studyset-detail', kwargs={'pk': self.object.study_set_id})

class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = 'cards/studyset_detail.html'

    def get_success_url(self):
        set = StudySet.objects.get(studyset=self.kwargs['pk'])
        return reverse('studyset-detail', kwargs={'pk': set.id})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class ArchivedCardListView(LoginRequiredMixin, ListView):
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

class StudySetDetailView(LoginRequiredMixin, DetailView):
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
    success_message = ('New Study Set created successfully!')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('studyset-detail', kwargs={'pk': self.object.pk})

class StudySetUpdateView(StudySetCreateView, UpdateView):
    success_message = 'Study set updated succesfully!'

    def get_success_url(self):
        return reverse('studyset-detail', kwargs={'pk': self.kwargs['pk']})

class StudySetDeleteView(LoginRequiredMixin, DeleteView):
    model = StudySet
    template_name = 'cards/studyset_detail.html'
    success_url = reverse_lazy('card-list')

# class FolderListView(ListView):
#     model = Folder
#     context_object_name = 'folders'
#     template_name = 'cards/card_list.html'
#
#     def get_queryset(self):
#         set = Folder.objects.all().filter(author=self.request.user)
#         return set

class FolderDetailView(LoginRequiredMixin, DetailView):
    model = Folder
    context_object_name = 'folder_detail'
    template_name = 'cards/folder_detail.html'

    def get_context_data(self, **kwargs):
        context = super(FolderDetailView, self).get_context_data()
        context['folder_studysets'] = StudySet.objects.all().filter(folder=self.kwargs['pk'])
        return context

class FolderCreateView(LoginRequiredMixin, CreateView):
    model = Folder
    fields = ('title', 'description')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('folder-detail', kwargs={'pk': self.object.pk})

class FolderUpdateView(FolderCreateView, UpdateView):

    def get_success_url(self):
        return reverse('folder-detail', kwargs={'pk': self.object.pk})

class FolderDeleteView(LoginRequiredMixin, DeleteView):
    model = Folder
    template_name = 'cards/folder_detail.html'
    success_url = reverse_lazy('card-list')

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



