from django.views.generic import CreateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import CustomUserRegisterForm

# Create your views here.

class UserRegisterView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = CustomUserRegisterForm
    template_name = 'common/register.html'
    success_url = reverse_lazy('login')
    success_message = 'New Account is created for %(first_name)'



