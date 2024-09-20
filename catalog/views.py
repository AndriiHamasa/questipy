from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

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


class ProjectDetailView(generic.DetailView):
    model = Project


class WorkerListView(generic.ListView):
    model = Worker
    paginate_by = 5


class WorkerDetailView(generic.DetailView):
    model = Worker


class ProjectTaskListView(generic.ListView):
    model = TaskType
    template_name = "catalog/task_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["project_pk"] = self.kwargs["pk"]
        return context

    def get_queryset(self):
        project_id = self.kwargs.get("pk")

        return Task.objects.filter(project__id=project_id)


class ProjectTaskCreateView(generic.CreateView):
    model = Task
    fields = "__all__"
    template_name = "catalog/project_task_form.html"

    def get_success_url(self):
        project_pk = self.kwargs.get("pk")

        return reverse_lazy("catalog:project-task-list", args=[project_pk])


class ProjectTaskDetailView(generic.DetailView):
    model = Task


class TaskTypeList(generic.ListView):
    model = TaskType
    paginate_by = 5


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("catalog:task-type-list")


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 5


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("catalog:position-list")