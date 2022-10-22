from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipes)

    def test_recipe_detail_view_return_404_if_no_recipes(self):
        response = self.client.get('recipes:recipe', kwargs={'category_id': 100})
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_correct_recipe(self):
        self.make_recipe(title='This is a detail page')

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        self.assertIn('This is a detail page', content)

    def test_recipe_detail_template_do_not_load_recipe_not_published(self):
        """If test recipe is_published False don't show"""
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': recipe.id}))

        self.assertEqual(response.status_code, 404)
