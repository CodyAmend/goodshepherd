from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..decorators import administrator_required
from ..forms import VolunteerSignUpForm
from ..models import User, Volunteer

@method_decorator([login_required, administrator_required], name='dispatch')
class VolunteerSignUpView(CreateView):
    model = User
    form_class = VolunteerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Volunteer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        new_user = form.save()
        Volunteer.objects.create(user=new_user)
        login(self.request, new_user)
        return redirect('/')