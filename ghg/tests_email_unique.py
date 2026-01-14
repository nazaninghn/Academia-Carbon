"""
Tests for email uniqueness validation
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ghg.forms import EmailSignupForm


class EmailUniquenessTest(TestCase):
    """Test that duplicate emails are prevented"""
    
    def setUp(self):
        """Create a test user"""
        self.test_email = 'test@example.com'
        self.test_user = User.objects.create_user(
            username=self.test_email,
            email=self.test_email,
            password='TestPass123!'
        )
    
    def test_duplicate_email_in_form(self):
        """Test that form rejects duplicate email"""
        form_data = {
            'email': self.test_email,
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'NewPass123!',
            'password2': 'NewPass123!',
        }
        form = EmailSignupForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('already registered', str(form.errors['email']))
    
    def test_unique_email_in_form(self):
        """Test that form accepts unique email"""
        form_data = {
            'email': 'newemail@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'NewPass123!',
            'password2': 'NewPass123!',
        }
        form = EmailSignupForm(data=form_data)
        
        self.assertTrue(form.is_valid())
    
    def test_case_insensitive_email(self):
        """Test that email comparison is case-insensitive"""
        form_data = {
            'email': 'TEST@EXAMPLE.COM',  # Same email, different case
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'NewPass123!',
            'password2': 'NewPass123!',
        }
        form = EmailSignupForm(data=form_data)
        
        # Should reject because email already exists (case-insensitive)
        self.assertFalse(form.is_valid())
    
    def test_signup_view_rejects_duplicate(self):
        """Test that signup view rejects duplicate email"""
        response = self.client.post('/en/signup/', {
            'email': self.test_email,
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'NewPass123!',
            'password2': 'NewPass123!',
        })
        
        # Should not create new user
        self.assertEqual(User.objects.filter(email=self.test_email).count(), 1)
        
        # Should show error message
        self.assertContains(response, 'already registered', status_code=200)
