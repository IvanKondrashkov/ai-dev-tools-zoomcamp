from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta
from .models import Todo


class TodoModelTest(TestCase):
    """Test cases for Todo model."""
    
    def setUp(self):
        """Set up test data."""
        self.todo = Todo.objects.create(
            title='Test TODO',
            description='Test description',
            due_date=timezone.now() + timedelta(days=1)
        )
    
    def test_todo_creation(self):
        """Test that a TODO can be created."""
        self.assertEqual(self.todo.title, 'Test TODO')
        self.assertFalse(self.todo.is_resolved)
        self.assertIsNotNone(self.todo.created_at)
    
    def test_todo_str(self):
        """Test the string representation of TODO."""
        self.assertEqual(str(self.todo), 'Test TODO')
    
    def test_todo_is_overdue(self):
        """Test the is_overdue method."""
        # Not overdue (future date)
        self.assertFalse(self.todo.is_overdue())
        
        # Overdue (past date)
        self.todo.due_date = timezone.now() - timedelta(days=1)
        self.todo.save()
        self.assertTrue(self.todo.is_overdue())
        
        # Resolved TODO should not be overdue
        self.todo.is_resolved = True
        self.todo.save()
        self.assertFalse(self.todo.is_overdue())


class TodoViewTest(TestCase):
    """Test cases for Todo views."""
    
    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.todo = Todo.objects.create(
            title='Test TODO',
            description='Test description'
        )
    
    def test_home_view(self):
        """Test the home view displays all TODOs."""
        response = self.client.get(reverse('todos:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test TODO')
        self.assertTemplateUsed(response, 'todos/home.html')
    
    def test_create_todo_get(self):
        """Test GET request to create TODO form."""
        response = self.client.get(reverse('todos:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
    
    def test_create_todo_post(self):
        """Test POST request to create a TODO."""
        data = {
            'title': 'New TODO',
            'description': 'New description',
            'due_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
        }
        response = self.client.post(reverse('todos:create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Todo.objects.filter(title='New TODO').exists())
    
    def test_edit_todo_get(self):
        """Test GET request to edit TODO form."""
        response = self.client.get(reverse('todos:edit', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
        self.assertContains(response, self.todo.title)
    
    def test_edit_todo_post(self):
        """Test POST request to update a TODO."""
        data = {
            'title': 'Updated TODO',
            'description': 'Updated description',
        }
        response = self.client.post(reverse('todos:edit', args=[self.todo.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated TODO')
    
    def test_delete_todo_get(self):
        """Test GET request to delete confirmation page."""
        response = self.client.get(reverse('todos:delete', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_confirm_delete.html')
    
    def test_delete_todo_post(self):
        """Test POST request to delete a TODO."""
        todo_id = self.todo.pk
        response = self.client.post(reverse('todos:delete', args=[todo_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(pk=todo_id).exists())
    
    def test_toggle_resolve(self):
        """Test toggling the resolved status of a TODO."""
        initial_status = self.todo.is_resolved
        response = self.client.get(reverse('todos:toggle', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertNotEqual(self.todo.is_resolved, initial_status)
    
    def test_empty_todo_list(self):
        """Test home view with no TODOs."""
        Todo.objects.all().delete()
        response = self.client.get(reverse('todos:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No TODOs')


class TodoFormTest(TestCase):
    """Test cases for Todo form."""
    
    def test_valid_form(self):
        """Test form with valid data."""
        from .forms import TodoForm
        data = {
            'title': 'Test TODO',
            'description': 'Test description',
        }
        form = TodoForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_missing_title(self):
        """Test form validation when title is missing."""
        from .forms import TodoForm
        data = {
            'description': 'Test description',
        }
        form = TodoForm(data=data)
        self.assertFalse(form.is_valid())

