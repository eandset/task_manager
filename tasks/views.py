from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Case, When, Value, IntegerField
from django.utils import timezone
from .forms import TaskForm
from .models import Task



def home(request):
    return render(request, "home.html")



@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user).annotate(
        priority_order=Case(
            When(priority=Task.Priority.HIGH, then=Value(0)),
            When(priority=Task.Priority.NORMAL, then=Value(1)),
            When(priority=Task.Priority.LOW, then=Value(2)),
            default=Value(3), output_field=IntegerField(),
        )
    ).order_by("completed", "priority_order", Case(When(due_date__isnull=True, then=Value(1)), default=Value(0)), "due_date", "-date_added")
    filter_name = request.GET.get("filter", "all")
    if filter_name == "active":
        tasks = tasks.filter(completed=False)
    elif filter_name == "completed":
        tasks = tasks.filter(completed=True)
    elif filter_name == "overdue":
        tasks = tasks.filter(completed=False, due_date__lt=timezone.now())
    return render(request, "tasks/list.html", {"tasks": tasks, "current_filter": filter_name, "now": timezone.now()})


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, "Задача создана.")
            return redirect("tasks:list")
    else:
        form = TaskForm()
    return render(request, "tasks/form.html", {"form": form, "page_title": "Новая задача", "button_text": "Создать задачу"})


@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id, owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Изменения сохранены.")
            return redirect("tasks:list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/form.html", {"form": form, "page_title": "Редактирование задачи", "button_text": "Сохранить", "task": task})


@login_required
@require_POST
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, owner=request.user)
    task.delete()
    messages.success(request, "Задача удалена.")
    return redirect("tasks:list")


@login_required
@require_POST
def task_toggle(request, task_id):
    task = get_object_or_404(Task, pk=task_id, owner=request.user)
    task.completed = not task.completed
    task.save(update_fields=["completed"])
    messages.success(request, "Статус задачи обновлён.")
    return redirect("tasks:list")
