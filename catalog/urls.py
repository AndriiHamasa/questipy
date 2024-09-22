from django.urls import path
from catalog.views import (
    index,
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    ProjectTaskListView,
    ProjectTaskCreateView,
    ProjectTaskDetailView,
    ProjectTaskToggleCompletedView,
    ProjectTaskAddWorkersView,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerPositionUpdateView,
    TaskTypeList,
    TaskTypeCreateView,
    PositionListView,
    PositionCreateView,

)

urlpatterns = [
    path("", index, name="index"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/create/", ProjectCreateView.as_view(), name="project-create"),
    path("projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"),
    path("projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"),
    path("projects/<int:pk>/tasks/", ProjectTaskListView.as_view(), name="project-task-list"),
    path("projects/<int:pk>/tasks/create/", ProjectTaskCreateView.as_view(), name="project-task-create"),
    path("projects/<int:project_pk>/tasks/<int:pk>/", ProjectTaskDetailView.as_view(), name="project-task-detail"),
    path("projects/<int:project_pk>/tasks/<int:pk>/task-toggle-completed/", ProjectTaskToggleCompletedView.as_view(), name="project-task-toggle-completed"),
    path("projects/<int:project_pk>/tasks/<int:pk>/add-workers/", ProjectTaskAddWorkersView.as_view(), name="project-task-add-workers"),
    # path("projects/workers/")
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/update/", WorkerPositionUpdateView.as_view(), name="worker-position-update"),
    path("task-types/", TaskTypeList.as_view(), name="task-type-list"),
    path("task-types/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("position/create/", PositionCreateView.as_view(), name="position-create"),
]

app_name = "catalog"
