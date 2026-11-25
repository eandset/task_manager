from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Task
User = get_user_model()

class TaskAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="StrongPass123!")
        self.other = User.objects.create_user(username="bob", password="StrongPass123!")
        self.task = Task.objects.create(owner=self.user, title="Alice task")

    def test_tasks_requires_login(self):
        response = self.client.get(reverse("tasks:list"))
        self.assertRedirects(response, f'{reverse("users:login")}?next={reverse("tasks:list")}')

    def test_list_only_own_tasks(self):
        Task.objects.create(owner=self.other, title="Bob task")
        self.client.login(username="alice", password="StrongPass123!")
        response = self.client.get(reverse("tasks:list"))
        self.assertContains(response, "Alice task")
        self.assertNotContains(response, "Bob task")

    def test_create_assigns_logged_in_owner(self):
        self.client.login(username="alice", password="StrongPass123!")
        response = self.client.post(reverse("tasks:create"), {"title":"Created by Alice", "description":"", "priority":"normal", "completed":""})
        self.assertRedirects(response, reverse("tasks:list"))
        created = Task.objects.get(title="Created by Alice")
        self.assertEqual(created.owner, self.user)

    def test_foreign_task_edit_and_delete_404(self):
        self.client.login(username="bob", password="StrongPass123!")
        self.assertEqual(self.client.get(reverse("tasks:edit", args=[self.task.pk])).status_code, 404)
        self.assertEqual(self.client.post(reverse("tasks:delete", args=[self.task.pk])).status_code, 404)

    def test_missing_task_404(self):
        self.client.login(username="alice", password="StrongPass123!")
        self.assertEqual(self.client.get(reverse("tasks:edit", args=[999999])).status_code, 404)

    def test_toggle_status_post_only(self):
        self.client.login(username="alice", password="StrongPass123!")
        url = reverse("tasks:toggle", args=[self.task.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.client.post(url)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)
        self.client.post(url)
        self.task.refresh_from_db()
        self.assertFalse(self.task.completed)

    def test_delete_post_only(self):
        self.client.login(username="alice", password="StrongPass123!")
        url = reverse("tasks:delete", args=[self.task.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.client.post(url)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
