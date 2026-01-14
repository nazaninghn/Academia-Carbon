"""
Tests for Google reCAPTCHA v3 Integration
Tests the captcha validation system for login and signup forms
"""

from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch, MagicMock
from ghg.captcha import ReCaptchaValidator, get_recaptcha_context

User = get_user_model()


class ReCaptchaValidatorTests(TestCase):
    """Test ReCaptchaValidator class"""
    
    @override_settings(RECAPTCHA_ENABLED=False)
    def test_captcha_disabled(self):
        """Test that validation passes when CAPTCHA is disabled"""
        result = ReCaptchaValidator.verify_token('fake_token', 'login')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['score'], 1.0)
        self.assertTrue(result.get('bypass'))
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SECRET_KEY='')
    def test_missing_secret_key(self):
        """Test that validation fails when secret key is missing"""
        result = ReCaptchaValidator.verify_token('fake_token', 'login')
        
        self.assertFalse(result['success'])
        self.assertEqual(result['score'], 0.0)
        self.assertIn('missing-secret-key', result['error_codes'])
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SECRET_KEY='test_secret')
    def test_missing_token(self):
        """Test that validation fails when token is missing"""
        result = ReCaptchaValidator.verify_token('', 'login')
        
        self.assertFalse(result['success'])
        self.assertEqual(result['score'], 0.0)
        self.assertIn('missing-input-response', result['error_codes'])
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SECRET_KEY='test_secret')
    @patch('ghg.captcha.requests.post')
    def test_successful_verification(self, mock_post):
        """Test successful reCAPTCHA verification"""
        # Mock Google's response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'score': 0.9,
            'action': 'login',
            'challenge_ts': '2024-01-01T00:00:00Z',
            'hostname': 'example.com'
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        result = ReCaptchaValidator.verify_token('valid_token', 'login', '127.0.0.1')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['score'], 0.9)
        self.assertEqual(result['action'], 'login')
        
        # Verify the request was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[1]['data']['secret'], 'test_secret')
        self.assertEqual(call_args[1]['data']['response'], 'valid_token')
        self.assertEqual(call_args[1]['data']['remoteip'], '127.0.0.1')
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SECRET_KEY='test_secret')
    @patch('ghg.captcha.requests.post')
    def test_failed_verification(self, mock_post):
        """Test failed reCAPTCHA verification"""
        # Mock Google's error response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': False,
            'error-codes': ['invalid-input-response']
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        result = ReCaptchaValidator.verify_token('invalid_token', 'login')
        
        self.assertFalse(result['success'])
        self.assertIn('error-codes', result)
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SECRET_KEY='test_secret')
    @patch('ghg.captcha.requests.post')
    def test_network_error(self, mock_post):
        """Test handling of network errors"""
        mock_post.side_effect = Exception('Network error')
        
        result = ReCaptchaValidator.verify_token('token', 'login')
        
        self.assertFalse(result['success'])
        self.assertEqual(result['score'], 0.0)
        self.assertIn('unknown-error', result['error_codes'])
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SECRET_KEY='test_secret')
    @patch('ghg.captcha.requests.post')
    def test_is_human_with_good_score(self, mock_post):
        """Test is_human returns True for good score"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'score': 0.8,
            'action': 'login'
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        is_human = ReCaptchaValidator.is_human('token', 'login', threshold=0.5)
        
        self.assertTrue(is_human)
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SECRET_KEY='test_secret')
    @patch('ghg.captcha.requests.post')
    def test_is_human_with_low_score(self, mock_post):
        """Test is_human returns False for low score"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'score': 0.3,
            'action': 'login'
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        is_human = ReCaptchaValidator.is_human('token', 'login', threshold=0.5)
        
        self.assertFalse(is_human)
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SECRET_KEY='test_secret')
    @patch('ghg.captcha.requests.post')
    def test_action_mismatch(self, mock_post):
        """Test that action mismatch is detected"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'score': 0.9,
            'action': 'signup'  # Different action
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        is_human = ReCaptchaValidator.is_human('token', 'login')  # Expecting 'login'
        
        self.assertFalse(is_human)
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SECRET_KEY='test_secret')
    @patch('ghg.captcha.requests.post')
    def test_get_score(self, mock_post):
        """Test get_score method"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'score': 0.75,
            'action': 'login'
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        score = ReCaptchaValidator.get_score('token', 'login')
        
        self.assertEqual(score, 0.75)


class ReCaptchaContextTests(TestCase):
    """Test reCAPTCHA context helper"""
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SITE_KEY='test_site_key')
    def test_context_with_captcha_enabled(self):
        """Test context when CAPTCHA is enabled"""
        context = get_recaptcha_context()
        
        self.assertTrue(context['RECAPTCHA_ENABLED'])
        self.assertEqual(context['RECAPTCHA_SITE_KEY'], 'test_site_key')
    
    @override_settings(RECAPTCHA_ENABLED=False, RECAPTCHA_SITE_KEY='test_site_key')
    def test_context_with_captcha_disabled(self):
        """Test context when CAPTCHA is disabled"""
        context = get_recaptcha_context()
        
        self.assertFalse(context['RECAPTCHA_ENABLED'])
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SITE_KEY='')
    def test_context_with_missing_site_key(self):
        """Test context when site key is missing"""
        context = get_recaptcha_context()
        
        self.assertFalse(context['RECAPTCHA_ENABLED'])


class LoginViewReCaptchaTests(TestCase):
    """Test reCAPTCHA integration in login view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )
        self.login_url = reverse('ghg:email_login')
    
    @override_settings(RECAPTCHA_ENABLED=False)
    def test_login_without_captcha(self):
        """Test login works when CAPTCHA is disabled"""
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'TestPass123!'
        })
        
        # Should redirect to index on success
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.session.get('_auth_user_id'))
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SECRET_KEY='test_secret')
    @patch('ghg.captcha.ReCaptchaValidator.is_human')
    def test_login_with_valid_captcha(self, mock_is_human):
        """Test login succeeds with valid CAPTCHA"""
        mock_is_human.return_value = True
        
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'TestPass123!',
            'recaptcha_token': 'valid_token'
        })
        
        # Should redirect to index on success
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.session.get('_auth_user_id'))
        
        # Verify is_human was called with correct parameters
        mock_is_human.assert_called_once()
        call_args = mock_is_human.call_args[0]
        self.assertEqual(call_args[0], 'valid_token')
        self.assertEqual(call_args[1], 'login')
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SECRET_KEY='test_secret')
    @patch('ghg.captcha.ReCaptchaValidator.is_human')
    def test_login_with_invalid_captcha(self, mock_is_human):
        """Test login fails with invalid CAPTCHA"""
        mock_is_human.return_value = False
        
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'TestPass123!',
            'recaptcha_token': 'invalid_token'
        })
        
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.client.session.get('_auth_user_id'))
        self.assertContains(response, 'Security verification failed')


class SignupViewReCaptchaTests(TestCase):
    """Test reCAPTCHA integration in signup view"""
    
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('ghg:email_signup')
        self.signup_data = {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
    
    @override_settings(RECAPTCHA_ENABLED=False)
    def test_signup_without_captcha(self):
        """Test signup works when CAPTCHA is disabled"""
        response = self.client.post(self.signup_url, self.signup_data)
        
        # Should redirect to index on success
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SECRET_KEY='test_secret')
    @patch('ghg.captcha.ReCaptchaValidator.is_human')
    def test_signup_with_valid_captcha(self, mock_is_human):
        """Test signup succeeds with valid CAPTCHA"""
        mock_is_human.return_value = True
        
        data = self.signup_data.copy()
        data['recaptcha_token'] = 'valid_token'
        
        response = self.client.post(self.signup_url, data)
        
        # Should redirect to index on success
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
        
        # Verify is_human was called with correct parameters
        mock_is_human.assert_called_once()
        call_args = mock_is_human.call_args[0]
        self.assertEqual(call_args[0], 'valid_token')
        self.assertEqual(call_args[1], 'signup')
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SECRET_KEY='test_secret')
    @patch('ghg.captcha.ReCaptchaValidator.is_human')
    def test_signup_with_invalid_captcha(self, mock_is_human):
        """Test signup fails with invalid CAPTCHA"""
        mock_is_human.return_value = False
        
        data = self.signup_data.copy()
        data['recaptcha_token'] = 'invalid_token'
        
        response = self.client.post(self.signup_url, data)
        
        # Should stay on signup page
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())
        self.assertContains(response, 'Security verification failed')
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SECRET_KEY='test_secret')
    @patch('ghg.captcha.ReCaptchaValidator.is_human')
    def test_signup_with_missing_captcha_token(self, mock_is_human):
        """Test signup fails when CAPTCHA token is missing"""
        mock_is_human.return_value = False
        
        response = self.client.post(self.signup_url, self.signup_data)
        
        # Should stay on signup page
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())


class ReCaptchaIntegrationTests(TestCase):
    """Integration tests for reCAPTCHA system"""
    
    def setUp(self):
        self.client = Client()
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SITE_KEY='test_site_key')
    def test_login_page_includes_recaptcha_script(self):
        """Test that login page includes reCAPTCHA script"""
        response = self.client.get(reverse('ghg:email_login'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'www.google.com/recaptcha/api.js')
        self.assertContains(response, 'test_site_key')
    
    @override_settings(RECAPTCHA_ENABLED=True, RECAPTCHA_SITE_KEY='test_site_key')
    def test_signup_page_includes_recaptcha_script(self):
        """Test that signup page includes reCAPTCHA script"""
        response = self.client.get(reverse('ghg:email_signup'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'www.google.com/recaptcha/api.js')
        self.assertContains(response, 'test_site_key')
    
    @override_settings(RECAPTCHA_ENABLED=False)
    def test_pages_without_recaptcha_when_disabled(self):
        """Test that pages don't include reCAPTCHA when disabled"""
        login_response = self.client.get(reverse('ghg:email_login'))
        signup_response = self.client.get(reverse('ghg:email_signup'))
        
        self.assertNotContains(login_response, 'www.google.com/recaptcha/api.js')
        self.assertNotContains(signup_response, 'www.google.com/recaptcha/api.js')
