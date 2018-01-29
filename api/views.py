from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import authenticate, login

from tastypie.models import ApiKey

from .models import Post
from .mixins import LoginRequiredMixin, PostMixin
from .forms import PostForm


class PostCreate(LoginRequiredMixin, PostMixin, CreateView):
    form_class = PostForm
    template_name = 'api/form.html'
    success_url = reverse_lazy('post:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.pub_date = timezone.now()
        return super(PostCreate, self).form_valid(form)


class PostUpdate(LoginRequiredMixin, PostMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'api/form.html'
    success_url = reverse_lazy('post:index')

    def form_valid(self, form):
        form.instance.pub_date = timezone.now()
        return super(PostUpdate, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_user_or_403(self.object.owner)
        return super(PostUpdate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_user_or_403(self.object.owner)
        return super(PostUpdate, self).post(request, *args, **kwargs)


class PostDelete(LoginRequiredMixin, PostMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post:index')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_user_or_403(self.object.owner)
        return super(PostDelete, self).post(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, PostMixin, FormView):
    template_name = 'api/profile.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('post:index')

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        try:
            api_key_obj = ApiKey.objects.get(user=self.request.user)
            api_key = api_key_obj.key
        except ApiKey.DoesNotExist:
            api_key = None

        context.update({
            'api_key': api_key
        })
        return context

    def get_form_kwargs(self):
        """ Our form requires the user. """

        kwargs = super(ProfileView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
        })

        return kwargs

    def form_valid(self, form):
        form.save()

        username = self.request.user.username
        password = self.request.POST['new_password2']

        # If we don't re-authenticate with the new password the user will get logged out.
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return super(ProfileView, self).form_valid(form)
