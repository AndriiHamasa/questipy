from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View

from catalog.forms import (
    ProjectForm,
    WorkerCreationForm,
    WorkerPositionUpdateForm,
    TaskCreationForm,
    TaskAddWorkersForm,
    ProjectNameSearchForm,
    WorkerUsernameSearchForm,
    TaskNameSearchForm,
    PositionNameSearchForm,
    TaskTypeNameSearchForm
)
from catalog.models import Project, Worker, TaskType, Task, Position


def index(request):
    project_list = Project.objects.all()
    worker_list = Worker.objects.all()

    context = {
        'project_list': project_list,
        'worker_list': worker_list,
    }

    return render(request, "catalog/index.html", context=context)


class ProjectListView(generic.ListView):
    model = Project
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = ProjectNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = ProjectNameSearchForm(self.request.GET)

        if form.is_valid():
            return Project.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return Project.objects.all()


class ProjectDetailView(generic.DetailView):
    model = Project


class ProjectCreateView(generic.CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('catalog:project-list')


class ProjectUpdateView(generic.UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('catalog:project-list')


class ProjectDeleteView(generic.DeleteView):
    model = Project
    success_url = reverse_lazy("catalog:project-list")

class WorkerListView(generic.ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = WorkerUsernameSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        form = WorkerUsernameSearchForm(self.request.GET)

        if form.is_valid():
            return get_user_model().objects.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return get_user_model().objects.all()



class WorkerDetailView(generic.DetailView):
    model = Worker


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy('catalog:worker-list')


class WorkerPositionUpdateView(generic.UpdateView):
    model = Worker
    form_class = WorkerPositionUpdateForm
    success_url = reverse_lazy('catalog:worker-list')


class ProjectTaskListView(generic.ListView):
    model = TaskType
    template_name = "catalog/task_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["project_pk"] = self.kwargs["pk"]
        context["project_name"] = Project.objects.get(pk=context["project_pk"])
        context["search_form"] = TaskNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = TaskNameSearchForm(self.request.GET)
        project_id = self.kwargs.get("pk")

        if form.is_valid():
            return Task.objects.filter(
                name__icontains=form.cleaned_data["name"],
                project_id=project_id
            )

        return Task.objects.filter(project__id=project_id)


class ProjectTaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskCreationForm
    template_name = "catalog/project_task_form.html"

    def get_success_url(self):
        project_pk = self.kwargs.get("pk")

        return reverse_lazy("catalog:project-task-list", args=[project_pk])

    def form_valid(self, form):
        project_pk = self.kwargs.get("pk")
        project = Project.objects.get(pk=project_pk)
        form.instance.project = project
        return super().form_valid(form)


class ProjectTaskDetailView(generic.DetailView):
    model = Task


class ProjectTaskToggleCompletedView(View):
    @staticmethod
    def post(request, **kwargs):
        task = Task.objects.get(pk=kwargs["pk"])
        task.is_completed = not task.is_completed
        task.save()
        return redirect("catalog:project-task-list", pk=kwargs["project_pk"])

class ProjectTaskAddWorkersView(generic.UpdateView):
    model = Task
    form_class = TaskAddWorkersForm
    template_name = "catalog/task_add_worker_form.html"

    def get_success_url(self):
        project_pk = self.kwargs.get("project_pk")
        return reverse_lazy("catalog:project-task-list", kwargs={"pk":project_pk})


class TaskTypeList(generic.ListView):
    model = TaskType
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskTypeNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = TaskTypeNameSearchForm(self.request.GET)

        if form.is_valid():
            return TaskType.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return TaskType.objects.all()


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("catalog:task-type-list")


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = PositionNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = PositionNameSearchForm(self.request.GET)

        if form.is_valid():
            return Position.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return Position.objects.all()


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("catalog:position-list")
