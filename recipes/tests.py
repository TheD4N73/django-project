from django.test import TestCase
from django.urls import reverse

class RecipeURLsTest(TestCase):
    def test_recipe_home_url(self):
        home_url = reverse('recipes:home')
        self.assertEqual(home_url, '/')