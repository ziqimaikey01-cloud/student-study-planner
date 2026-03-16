from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Course, Assignment
# Create your tests here.



class CourseModelTest(TestCase):

    def test_course_str(self):
        course = Course.objects.create(
            name="Internet Technology",
            code="COMPSCI5012"
        )
        self.assertEqual(str(course), "Internet Technology")


class AssignmentModelTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            name="Test Course",
            code="TEST101"
        )

    def test_assignment_str(self):
        assignment = Assignment.objects.create(
            course=self.course,
            title="Test Assignment",
            due_date=timezone.now()
        )
        self.assertEqual(str(assignment), "Test Assignment")

    def test_assignment_default_completed(self):
        assignment = Assignment.objects.create(
            course=self.course,
            title="Test Assignment",
            due_date=timezone.now()
        )
        self.assertFalse(assignment.completed)


class ViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_logged_in(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)