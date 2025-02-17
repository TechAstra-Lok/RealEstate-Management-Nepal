from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.
class HomeViewTest(TestCase):
    
    def setUp(self):
        """Create a test user."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_home_view_for_authenticated_user(self):
        """Test home view redirect for authenticated users."""
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        
        # Make a request to the home page
        response = self.client.get(reverse('home'))
        
        # Check that the response is a redirect to the dashboard
        self.assertRedirects(response, reverse('dashboard'), status_code=302)

    def test_home_view_for_unauthenticated_user(self):
        """Test home view for unauthenticated users."""
        # Make a request to the home page without logging in
        response = self.client.get(reverse('home'))
        
        # Check that the response is a normal 200 OK response (not a redirect)
        self.assertEqual(response.status_code, 200)
        
        # Check that the unauthenticated navbar links are displayed
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Register')

    def test_home_view_login_redirect_when_authenticated(self):
        """Test that unauthenticated users are redirected to login if they visit a protected page"""
        # Make a request to the dashboard page without logging in
        response = self.client.get(reverse('dashboard'))
        
        # Check that the response redirects to login
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("dashboard")}', status_code=302)