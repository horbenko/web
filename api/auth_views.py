from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        # Save the new user first
        form.save()
        # Get the username and password
        username = self.request.POST['username']
        password = self.request.POST['password1']
        # Authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)
