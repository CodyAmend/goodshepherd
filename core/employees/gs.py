from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..decorators import administrator_required

@method_decorator([login_required, administrator_required], name='dispatch')
class SignUpView(TemplateView):
    template_name = 'registration/signup.html'
