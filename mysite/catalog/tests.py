from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.models import Product
import base64
import json

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        
        self.product1 = Product.objects.create(
            name='Test Product 1',
            description='Test Description 1',
            price=100.00,
            in_stock=True
        )
        self.product2 = Product.objects.create(
            name='Test Product 2',
            description='Test Description 2',
            price=200.00,
            in_stock=True
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('catalog:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_list.html')
        self.assertContains(response, 'Test Product 1')
        self.assertContains(response, 'Test Product 2')

    def test_ajax_get_products(self):
        response = self.client.get(reverse('ajax_get_products'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = json.loads(response.content)
        self.assertIn('products', data)
        
        self.assertTrue(len(data['products']) > 0)

    def test_ajax_add_to_cart_post(self):
        self.client.login(username='testuser', password='testpassword123')
        
        response = self.client.post(
            reverse('ajax_add_to_cart'),
            data=json.dumps({'product_id': self.product1.pk}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertIn('cart', data)
        self.assertIn(str(self.product1.pk), data['cart'])
        self.assertEqual(data['cart'][str(self.product1.pk)], 1)


    def test_ajax_remove_from_cart_post(self):
        self.client.login(username='testuser', password='testpassword123')
        
        self.client.post(
            reverse('ajax_add_to_cart'),
            data=json.dumps({'product_id': self.product1.pk}),
            content_type='application/json'
        )
        
        response = self.client.post(
            reverse('ajax_remove_from_cart'),
            data=json.dumps({'product_id': self.product1.pk}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertNotIn(str(self.product1.pk), data['cart'])

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_view_post(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'testpassword123'}
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('homepage:home'))

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_view_post(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'newuser',
                'password1': 'complexpassword123',
                'password2': 'complexpassword123'
            }
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage:home'))
        
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword123')
        
        response = self.client.get(reverse('homepage:home'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('logout'))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage:home'))

    def test_cart_view(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')

    def test_homepage_view(self):
        response = self.client.get(reverse('homepage:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/index.html')

    def test_about_view(self):
        response = self.client.get(reverse('about:description'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/index.html')

    def test_product_list_ajax_view(self):
        response = self.client.get(reverse('product_list_ajax'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_list_ajax.html')

    def test_invalid_url_returns_404(self):
        response = self.client.get('/nonexistent-url/')
        self.assertEqual(response.status_code, 404)


class ModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=150.00,
            in_stock=True
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.description, 'Test Description')
        self.assertEqual(self.product.price, 150.00)
        self.assertTrue(self.product.in_stock)

    def test_product_str_representation(self):
        self.assertEqual(str(self.product), 'Test Product')

        
        with self.assertRaises(Exception):
            product.full_clean()


class FormTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }

    def test_valid_registration_form(self):
        from django.contrib.auth.forms import UserCreationForm
        
        form = UserCreationForm(data=self.user_data)
        self.assertTrue(form.is_valid())

    def test_invalid_registration_form(self):
        from django.contrib.auth.forms import UserCreationForm
        
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'differentpassword'
        
        form = UserCreationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class MiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )

    def test_basic_auth_middleware(self):
        auth_header = 'Basic ' + base64.b64encode(b'testuser:testpassword123').decode('utf-8')
        
        response = self.client.get(
            reverse('homepage:home'),
            HTTP_AUTHORIZATION=auth_header
        )
        
        self.assertEqual(response.status_code, 200)