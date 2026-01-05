from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import RegisterUserForm, LoginUserForm, AddCommentForm
from .models import Category_Tasks, Category_Tasks_Filter, Task, Category_Options, Theory_category, Theory_item, Comment
from django.views.generic import CreateView, ListView, DetailView


nav = [
    {'title': "Home", 'url_name': 'home'},
    {'title': "Options", 'url_name': 'options'},
    {'title': "Tasks", 'url_name': 'tasks'},
    {'title': "Theory", 'url_name': 'themes'}
]


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')


def forbidden_403(request):
    return HttpResponseForbidden()


class Home(ListView):
    model = Task
    template_name = 'tasks/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        context['title'] = 'Home page'
        context['options'] = 'Options'
        context['tasks'] = 'Tasks'
        context['theory'] = 'Theory'
        return context


class Tasks(ListView):
    model = Category_Tasks
    template_name = 'tasks/tasks.html'
    context_object_name = 'categories'
    extra_context = {'title': 'Tasks'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        count_tasks = Category_Tasks.objects.all()
        context['categories'] = {}
        for i in range(1, len(count_tasks) + 1):
            filters = Category_Tasks_Filter.objects.filter(cat__id=i)
            if filters.exists():
                context['categories'][filters] = count_tasks[i - 1]
        return context


class Task_Object(DetailView):
    model = Task
    template_name = 'tasks/task.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        task_id = self.kwargs['task_id']
        context['title'] = f"Task {task_id}"
        context['title_task'] = task_id
        context['comments'] = Comment.objects.filter(post=task_id, is_published=True)
        context['form'] = AddCommentForm()
        try:
            task = Task.objects.get(id=task_id)
            context['theme'] = task.filter
        except Task.DoesNotExist:
            context['theme'] = None
        return context

    def get_object(self, **kwargs):
        return Task.objects.get(id=self.kwargs['task_id'])

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = AddCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post_id = self.kwargs['task_id']
                comment.save()
        return redirect(request.META.get('HTTP_REFERER', 'home'))


class Options(ListView):
    model = Category_Options
    template_name = 'tasks/options.html'
    context_object_name = 'options'
    extra_context = {'title': 'Options'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        return context


class Catalog_tasks(ListView):
    model = Task
    template_name = 'tasks/list_tasks.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        context['title'] = f"Category {self.kwargs['cat_id']}"
        context['task_cat'] = self.kwargs['cat_id']
        return context

    def get_queryset(self):
        return Task.objects.filter(cat_id=self.kwargs['cat_id'], is_published=True)


class Catalog_tasks_filter(ListView):
    model = Category_Tasks_Filter
    template_name = 'tasks/list_tasks.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        filter_obj = Category_Tasks_Filter.objects.filter(slug=self.kwargs['filter_slug']).first()
        if filter_obj:
            context['task_cat'] = filter_obj.cat.id
            context['title'] = f"Category {filter_obj.cat.id}"
        else:
            context['task_cat'] = None
            context['title'] = "Tasks"
        return context

    def get_queryset(self):
        filter_obj = Category_Tasks_Filter.objects.filter(slug=self.kwargs['filter_slug']).first()
        if filter_obj:
            return Task.objects.filter(filter=filter_obj, is_published=True)
        return Task.objects.none()


class Catalog_option_tasks(ListView):
    model = Category_Options
    template_name = 'tasks/list_option.html'
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        context['title'] = f"Option {self.kwargs['opt_id']}"
        return context

    def get_queryset(self):
        option = Category_Options.objects.filter(id=self.kwargs['opt_id'], is_published=True).first()
        if not option:
            return {}

        tasks = {}
        for i in range(1, 19):
            field_name = f'id_number_{i}'
            if hasattr(option, field_name):
                task_id_str = getattr(option, field_name)
                if task_id_str and task_id_str.strip():
                    try:
                        task_id = int(task_id_str)
                        tasks[i] = Task.objects.get(id=task_id, is_published=True)
                    except (Task.DoesNotExist, ValueError):
                        continue
        return tasks


class Themes(ListView):
    model = Theory_category
    template_name = 'tasks/themes.html'
    extra_context = {'title': 'Theory'}
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        context['dct'] = {}
        categories = Theory_category.objects.all()
        for category in categories:
            items = Theory_item.objects.filter(cat=category, is_published=True)
            if items.exists():
                context['dct'][category.category] = items
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        context['title'] = 'Registration'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = nav
        context['title'] = 'Login'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


@login_required
@require_POST
def logout_user(request):
    logout(request)
    return redirect('login')
