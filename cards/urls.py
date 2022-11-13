from django.urls import path
from django.views.generic import TemplateView
from .views import CardListView, CardCreateView

urlpatterns = [
    # path('', TemplateView.as_view(template_name='cards/home.html'), name='home')
    path('', CardListView.as_view(), name='card-list'),
    path('card/new', CardCreateView.as_view(), name='card-form'),
]