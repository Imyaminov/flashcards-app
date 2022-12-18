from django.urls import path
from django.views.generic import TemplateView
from .views import (
    CardListView,
    CardCreateView,
    CardUpdateView,
    CardDeleteView,
    BoxView,
    ArchivedCardListView,
    change_status,
    StudySetCreateView,
    FolderCreateView,
    # StudySetListView,
    # FolderListView,
    StudySetDetailView,
    StudySetUpdateView,
    FolderDetailView,
    FolderNoneSetList,
    FolderSetRemove,
    FolderSetAdd,
)

urlpatterns = [
    # path('', TemplateView.as_view(template_name='cards/home.html'), name='home')
    path('', CardListView.as_view(), name='card-list'),
    path('card/new', CardCreateView.as_view(), name='card-create'),
    path('card/<int:pk>/update', CardUpdateView.as_view(), name='card-update'),
    path('card/<int:pk>/delete', CardDeleteView.as_view(), name='card-delete'),
    path('box/<int:box_num>', BoxView.as_view(), name='box'),
    path('archive/<int:pk>', change_status, name='change-status'),
    path('archived_cards/', ArchivedCardListView.as_view(), name='archived-cards'),
    path('studyset/new', StudySetCreateView.as_view(), name='studyset-create'),
    path('folder/new', FolderCreateView.as_view(), name='folder-create'),
    # path('studyset_list', StudySetListView.as_view(), name='studyset-list'),
    # path('folder_list', FolderListView.as_view(), name='folder-list'),
    path('studyset/<int:pk>', StudySetDetailView.as_view(), name='studyset-detail'),
    path('studyset/<int:pk>/update', StudySetUpdateView.as_view(), name='studyset-update'),
    path('folder/<int:pk>', FolderDetailView.as_view(), name='folder-detail'),
    path('folder/set/<int:pk>/remove', FolderSetRemove, name='folder-set-remove'),
    path('folder/<int:folder_id>/set/<int:set_id>/add', FolderSetAdd, name='folder-set-add'),
    path('folder/<int:folder>/set-add', FolderNoneSetList, name='folder-none-set'),
]