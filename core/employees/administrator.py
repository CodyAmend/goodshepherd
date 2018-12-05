from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..decorators import administrator_required
from ..forms import AdministratorSignUpForm
from ..models import User, Administrator

@method_decorator([login_required, administrator_required], name='dispatch')
class AdministratorSignUpView(CreateView):
    model = User
    form_class = AdministratorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Administrator'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        Administrator.objects.create(user=user)
        login(self.request, user)
        return redirect('/')