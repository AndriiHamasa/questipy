from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View

from catalog.forms import (
    ProjectForm,
    WorkerCreationForm,
    WorkerPositionUpdateForm,
    TaskForm,
    TaskAddWorkersForm,
    ProjectNameSearchForm,
    WorkerUsernameSearchForm,
    TaskNameSearchForm,
    PositionNameSearchForm,
    TaskTypeNameSearchForm,
    ProjectAddWorkerForm,
)
from catalog.models import Project, Worker, TaskType, Task, Position


def index(request):
    project_list = Project.objects.all()
    worker_list = Worker.objects.all()

    context = {
        "project_list": project_list,
        "worker_list": worker_list,
    }

    return render(request, "catalog/index.html", context=context)


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = ProjectNameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = ProjectNameSearchForm(self.request.GET)

        if form.is_valid():
            return Project.objects.filter(name__icontains=form.cleaned_data["name"])

        return Project.objects.all()


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("catalog:project-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("catalog:project-list")


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("catalog:project-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
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


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("catalog:worker-list")


class WorkerPositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerPositionUpdateForm
    template_name = "catalog/worker-update-position-form.html"
    success_url = reverse_lazy("catalog:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("catalog:worker-list")


class ProjectTaskListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "catalog/task_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["project_pk"] = self.kwargs["pk"]
        context["project_name"] = Project.objects.get(pk=context["project_pk"])
        context["search_form"] = TaskNameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = TaskNameSearchForm(self.request.GET)
        project_id = self.kwargs.get("pk")

        if form.is_valid():
            return Task.objects.filter(
                name__icontains=form.cleaned_data["name"], project_id=project_id
            )

        return Task.objects.filter(project__id=project_id)


class ProjectTaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "catalog/project_task_form.html"

    def get_initial(self):
        initial = super().get_initial()
        project_pk = self.kwargs.get("pk")
        initial["project_pk"] = project_pk
        return initial

    def get_success_url(self):
        project_pk = self.kwargs.get("pk")

        return reverse_lazy("catalog:project-task-list", args=[project_pk])

    def form_valid(self, form):
        project_pk = self.kwargs.get("pk")
        project = Project.objects.get(pk=project_pk)
        form.instance.project = project
        return super().form_valid(form)


class ProjectTaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "catalog/project_task_form.html"

    def get_success_url(self):
        project_pk = self.kwargs.get("project_pk")

        return reverse_lazy("catalog:project-task-list", args=[project_pk])

    def form_valid(self, form):
        project_pk = self.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_pk)
        form.instance.project = project
        return super().form_valid(form)


class ProjectTaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class ProjectTaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "catalog/confirm_delete.html"

    def get_success_url(self):
        project_pk = self.kwargs.get("project_pk")

        return reverse_lazy("catalog:project-task-list", kwargs={"pk": project_pk})


class ProjectAddWorkersView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectAddWorkerForm
    template_name = "catalog/project_add_worker_form.html"

    def get_success_url(self):
        project_pk = self.kwargs.get("pk")
        return reverse_lazy("catalog:project-detail", kwargs={"pk": project_pk})


class ProjectTaskToggleCompletedView(LoginRequiredMixin, View):
    @staticmethod
    def post(request, **kwargs):
        task = Task.objects.get(pk=kwargs["pk"])
        task.is_completed = not task.is_completed
        task.save()
        return redirect("catalog:project-task-list", pk=kwargs["project_pk"])


class ProjectTaskAddWorkersView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskAddWorkersForm
    template_name = "catalog/task_add_worker_form.html"

    def get_initial(self):
        initial = super().get_initial()
        project_pk = self.kwargs.get("project_pk")
        initial["project_pk"] = project_pk
        return initial

    def get_success_url(self):
        project_pk = self.kwargs.get("project_pk")
        return reverse_lazy("catalog:project-task-list", kwargs={"pk": project_pk})


class TaskTypeList(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskTypeNameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = TaskTypeNameSearchForm(self.request.GET)

        if form.is_valid():
            return TaskType.objects.filter(name__icontains=form.cleaned_data["name"])

        return TaskType.objects.all()


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("catalog:task-type-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name in form.fields:
            form.fields[field_name].widget.attrs.update(
                {"style": "background-color: #1a252f; color: white;"}
            )
        return form


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("catalog:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("catalog:task-type-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name in form.fields:
            form.fields[field_name].widget.attrs.update(
                {"style": "background-color: #1a252f; color: white;"}
            )
        return form


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = PositionNameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = PositionNameSearchForm(self.request.GET)

        if form.is_valid():
            return Position.objects.filter(name__icontains=form.cleaned_data["name"])

        return Position.objects.all()


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("catalog:position-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name in form.fields:
            form.fields[field_name].widget.attrs.update(
                {"style": "background-color: #1a252f; color: white;"}
            )
        return form


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("catalog:position-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name in form.fields:
            form.fields[field_name].widget.attrs.update(
                {"style": "background-color: #1a252f; color: white;"}
            )
        return form


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("catalog:position-list")
