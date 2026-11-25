from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name="Task", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("title", models.CharField(max_length=200)),
        ("description", models.TextField(blank=True)),
        ("date_added", models.DateTimeField(auto_now_add=True)),
        ("due_date", models.DateTimeField(blank=True, null=True)),
        ("priority", models.CharField(choices=[("low", "Низкий"), ("normal", "Обычный"), ("high", "Высокий")], default="normal", max_length=10)),
        ("completed", models.BooleanField(default=False)),
        ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to=settings.AUTH_USER_MODEL)),
    ], options={"ordering": ["completed", "-priority", "due_date"]}),]
