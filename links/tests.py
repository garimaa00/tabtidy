from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import SavedLink


class TabTidyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPassword123!'
        )
        self.client.force_login(self.user)

        self.link = SavedLink.objects.create(
            owner=self.user,
            title='Django Docs',
            url='https://docs.djangoproject.com/',
            category='Coding',
        )

    def test_dashboard_loads(self):
        response = self.client.get(reverse('link_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Docs')

    def test_create_link(self):
        response = self.client.post(
            reverse('link_create'),
            {
                'title': 'Python Docs',
                'url': 'https://docs.python.org/3/',
                'category': 'Learning',
                'note': 'Learn Python',
                'is_visited': '',
            },
        )

        self.assertRedirects(response, reverse('link_list'))
        self.assertTrue(
            SavedLink.objects.filter(title='Python Docs').exists()
        )

    def test_search_links(self):
        response = self.client.get(
            reverse('link_list'),
            {'q': 'Django'},
        )

        self.assertContains(response, 'Django Docs')
    
    def test_toggle_requires_post(self):
        response = self.client.get(
            reverse('link_toggle_visited', args=[self.link.pk])
        )

        self.assertRedirects(response, reverse('link_list'))

        self.link.refresh_from_db()
        self.assertFalse(self.link.is_visited)


    def test_toggle_visited(self):
        response = self.client.post(
            reverse('link_toggle_visited', args=[self.link.pk])
        )

        self.assertRedirects(response, reverse('link_list'))
        self.link.refresh_from_db()
        self.assertTrue(self.link.is_visited)

    def test_delete_requires_confirmation(self):
        response = self.client.get(
            reverse('link_delete', args=[self.link.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            SavedLink.objects.filter(pk=self.link.pk).exists()
        )

    def test_delete_link(self):
        response = self.client.post(
            reverse('link_delete', args=[self.link.pk])
        )

        self.assertRedirects(response, reverse('link_list'))
        self.assertFalse(
            SavedLink.objects.filter(pk=self.link.pk).exists()
        )

