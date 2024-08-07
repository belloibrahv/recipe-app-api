"""
Tests for models
"""
from unittest.mock import patch
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='testuser@mail.com', password='testpass123',):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating user with an email is successful"""
        email = "testuser@example.com"
        password = "testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new user"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['test3@example.Com', 'test3@example.com'],
            ['test4@exaMple.Com', 'test4@example.com'],
            ['test5@EXAMPLE.COM', 'test5@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email,
                'test123'
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a valueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_super_user(self):
        """Test creating a super user"""
        user = get_user_model().objects.create_superuser(
            'test@smaple.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def create_recipe(self):
        """Test create a recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@sample.com',
            'test123',
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.30'),
            description='Sample recipe description.'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successful."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name="Ingredient1"
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test_uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')
