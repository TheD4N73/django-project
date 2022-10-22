from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 100}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_404_if_no_recipes(self):
        response = self.client.get('recipes:category', kwargs={'category_id': 100})
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        self.make_recipe(title='This is a category test')

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn('This is a category test', content)

    def test_recipe_category_template_do_not_load_recipe_not_published(self):
        """If test recipe is_published False don't show"""
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': recipe.category.id}))

        self.assertEqual(response.status_code, 404)
