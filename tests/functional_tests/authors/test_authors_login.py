import pytest
from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pas'
        user = User.objects.create_user(username='myuser', password=string_password)

        # User open login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User see the form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # User insert your username and password
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # User send form
        form.submit()

        # User see the login successfully message
        self.assertIn(
            f'Your are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid(self):
        # User open the login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User see login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # Try send blank data
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        username_field.send_keys(' ')
        password_field.send_keys(' ')

        # User send form
        form.submit()

        # See a error message
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_invalid_credentials(self):
        # User open the login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User see login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # User send data with errors
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        username_field.send_keys('invalid_user')
        password_field.send_keys('invalid_password')

        # User send form
        form.submit()

        # See a error message
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
