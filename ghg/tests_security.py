"""
Tests for security features (Account Lockout)
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ghg.security import AccountLockout
from django.core.cache import cache


class AccountLockoutTest(TestCase):
    """Test account lockout functionality"""
    
    def setUp(self):
        """Create test user and client"""
        self.client = Client()
        self.test_email = 'test@example.com'
        self.test_password = 'TestPass123!'
        
        self.user = User.objects.create_user(
            username=self.test_email,
            email=self.test_email,
            password=self.test_password
        )
        
        # Clear cache before each test
        cache.clear()
    
    def tearDown(self):
        """Clean up after tests"""
        cache.clear()
    
    def test_failed_login_increments_counter(self):
        """Test that failed login increments the counter"""
        # Try to login with wrong password
        response = self.client.post(reverse('ghg:email_login'), {
            'username': self.test_email,
            'password': 'WrongPassword123!'
        })
        
        # Check that failed attempts were recorded
        attempts = AccountLockout.get_failed_attempts(self.test_email)
        self.assertEqual(attempts, 1)
    
    def test_successful_login_resets_counter(self):
        """Test that successful login resets the counter"""
        # First, create some failed attempts
        AccountLockout.increment_failed_attempts(self.test_email)
        AccountLockout.increment_failed_attempts(self.test_email)
        
        # Now login successfully
        response = self.client.post(reverse('ghg:email_login'), {
            'username': self.test_email,
            'password': self.test_password
        })
        
        # Check that counter was reset
        attempts = AccountLockout.get_failed_attempts(self.test_email)
        self.assertEqual(attempts, 0)
    
    def test_account_locks_after_max_attempts(self):
        """Test that account locks after max failed attempts"""
        # Make 5 failed login attempts
        for i in range(5):
            self.client.post(reverse('ghg:email_login'), {
                'username': self.test_email,
                'password': 'WrongPassword123!'
            })
        
        # Check that account is locked
        self.assertTrue(AccountLockout.is_locked(self.test_email))
    
    def test_locked_account_cannot_login(self):
        """Test that locked account cannot login even with correct password"""
        # Lock the account
        AccountLockout.lock_account(self.test_email)
        
        # Try to login with correct password
        response = self.client.post(reverse('ghg:email_login'), {
            'username': self.test_email,
            'password': self.test_password
        })
        
        # Should not be logged in
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        
        # Should show lockout message
        messages = list(response.context['messages'])
        self.assertTrue(any('locked' in str(m).lower() for m in messages))
    
    def test_unlock_account_command(self):
        """Test manual account unlock"""
        # Lock the account
        AccountLockout.lock_account(self.test_email)
        self.assertTrue(AccountLockout.is_locked(self.test_email))
        
        # Unlock it
        AccountLockout.unlock_account(self.test_email)
        self.assertFalse(AccountLockout.is_locked(self.test_email))
    
    def test_attempts_remaining(self):
        """Test getting attempts remaining"""
        # No failed attempts yet
        remaining = AccountLockout.get_attempts_remaining(self.test_email)
        self.assertEqual(remaining, 5)
        
        # After 2 failed attempts
        AccountLockout.increment_failed_attempts(self.test_email)
        AccountLockout.increment_failed_attempts(self.test_email)
        remaining = AccountLockout.get_attempts_remaining(self.test_email)
        self.assertEqual(remaining, 3)
    
    def test_lockout_time_remaining(self):
        """Test getting lockout time remaining"""
        # Not locked
        remaining = AccountLockout.get_lockout_time_remaining(self.test_email)
        self.assertEqual(remaining, 0)
        
        # Lock account
        AccountLockout.lock_account(self.test_email)
        remaining = AccountLockout.get_lockout_time_remaining(self.test_email)
        self.assertGreater(remaining, 0)
        self.assertLessEqual(remaining, 30 * 60)  # Max 30 minutes
