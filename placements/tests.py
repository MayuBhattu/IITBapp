"""Unit tests for Placements."""
from django.conf import settings
from rest_framework.test import APITestCase
from placements.models import BlogEntry
from login.tests import get_new_user

class PlacementsTestCase(APITestCase):
    """Test placements endpoints."""

    entry1 = None

    def setUp(self):
        # Create dummies
        self.entry1 = BlogEntry.objects.create(title="PEntry1", blog_url=settings.PLACEMENTS_URL)
        BlogEntry.objects.create(title="PEntry2", blog_url=settings.PLACEMENTS_URL)
        BlogEntry.objects.create(title="TEntry1", blog_url=settings.TRAINING_BLOG_URL)
        BlogEntry.objects.create(title="TEntry2", blog_url=settings.TRAINING_BLOG_URL)
        BlogEntry.objects.create(title="TEntry3", blog_url=settings.TRAINING_BLOG_URL)

    def test_placement_other(self):
        """Check misc parameters of Placement."""
        self.assertEqual(str(self.entry1), self.entry1.title)

    def test_placement_get(self):
        """Check auth before getting placements."""

        # Try without authentication
        url = '/api/placement-blog'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

        # Try after authentication
        user = get_new_user()
        self.client.force_authenticate(user) # pylint: disable=E1101
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_training_get(self):
        """Check auth before getting training blog."""

        # Try without authentication
        url = '/api/training-blog'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

        # Try after authentication
        user = get_new_user()
        self.client.force_authenticate(user) # pylint: disable=E1101
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
