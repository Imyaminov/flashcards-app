from django.urls import path
from django.views.generic import TemplateView
from .views import (
    CardListView,
    CardCreateView,
    CardUpdateView,
    BoxView,
    ArchivedCardListView,
    change_status,
    StudySetCreateView,
    FolderCreateView
)

urlpatterns = [
    # path('', TemplateView.as_view(template_name='cards/home.html'), name='home')
    path('', CardListView.as_view(), name='card-list'),
    path('card/new', CardCreateView.as_view(), name='card-create'),
    path('card/<int:pk>/update', CardUpdateView.as_view(), name='card-update'),
    path('box/<int:box_num>', BoxView.as_view(), name='box'),
    path('archive/<int:pk>', change_status, name='change-status'),
    path('archived_cards/', ArchivedCardListView.as_view(), name='archived-cards'),
    path('studyset/new', StudySetCreateView.as_view(), name='studyset-create'),
    path('folder/new', FolderCreateView.as_view(), name='folder-create'),
]