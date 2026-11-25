from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        required=False,
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}, format="%Y-%m-%dT%H:%M"),
        help_text="Необязательно",
    )

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "priority", "completed"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, подготовить отчёт"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Подробности задачи..."}),
            "priority": forms.Select(attrs={"class": "form-control"}),
            "completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
