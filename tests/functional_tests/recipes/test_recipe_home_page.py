import pytest
from .base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest.mock import patch


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_error_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here!', body.text)

    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()

        # User open page
        self.browser.get(self.live_server_url)

        # See a search with text "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe..."]'
        )

        # Click in input and type "Recipe title 1" for search this recipe
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(title_needed, self.browser.find_element(By.CLASS_NAME, 'main-content-list').text)

        self.sleep()

    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        # User open page
        self.browser.get(self.live_server_url)

        # See a pagination and click in page 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # See 2 more recipes in page 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
