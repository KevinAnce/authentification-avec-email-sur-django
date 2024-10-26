from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UserTests(TestCase):

    def setUp(self):
        self.email = 'testuser@example.com'
        self.password = 'Testpass123'
        self.user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password
        )

    def test_create_user_with_email(self):
        """Vérifie qu'un utilisateur peut être créé avec une adresse email"""
        user = get_user_model().objects.get(email=self.email)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))

    def test_user_login(self):
        """Teste la connexion de l'utilisateur avec l'email et le mot de passe"""
        login = self.client.login(email=self.email, password=self.password)
        self.assertTrue(login)

    def test_signup_view(self):
        """Teste l'affichage de la page d'inscription et la création d'un utilisateur"""
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

        new_user_email = 'newuser@example.com'
        response = self.client.post(reverse('users:signup'), {
            'email': new_user_email,
            'password1': 'Newpass123',
            'password2': 'Newpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirection après inscription
        new_user = get_user_model().objects.get(email=new_user_email)
        self.assertEqual(new_user.email, new_user_email)
