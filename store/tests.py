from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product, Order, OrderItem, Review
import json

class FullStackStoreTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Regular player user
        self.regular_user = User.objects.create_user(
            username='player_viktor',
            password='Password123!',
            email='viktor@court.com'
        )

        # Admin user (staff & superuser)
        self.admin_user = User.objects.create_superuser(
            username='store_admin',
            password='AdminPassword123!',
            email='admin@smashpoint.com'
        )

        # Create Category
        self.category = Category.objects.create(name='Racquets', slug='racquets')

        # Create Product
        self.product = Product.objects.create(
            category=self.category,
            name='Yonex Astrox 100ZZ',
            slug='yonex-astrox-100zz',
            brand='Yonex',
            price=18990.00,
            image_url='images/astrox100zz.png',
            description='Hyper Slim shaft for maximum smash power.',
            specs='4U/G5 • Extra Stiff • 28 LBS',
            badge='Hyper Heavy',
            rating=4.9,
            is_featured=True,
            stock_quantity=10,
            is_in_stock=True
        )

    def test_anonymous_user_lands_on_home_page_not_logged_in(self):
        """Verify visiting the store does NOT pre-log in as admin."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Sign In')
        self.assertNotContains(response, 'Sign Out')

    def test_regular_player_login_redirects_to_storefront(self):
        """Regular customer login redirects to storefront homepage."""
        response = self.client.post(reverse('login'), {
            'username': 'player_viktor',
            'password': 'Password123!',
            'next': ''
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        # Should land on home page with welcome message
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertFalse(response.context['user'].is_staff)
        self.assertContains(response, 'player_viktor')
        self.assertContains(response, 'My Orders')

    def test_admin_credentials_login_redirects_to_admin_portal(self):
        """Logging in with admin credentials redirects directly to /admin/ portal."""
        response = self.client.post(reverse('login'), {
            'username': 'store_admin',
            'password': 'AdminPassword123!',
            'next': ''
        })
        # Must redirect to /admin/
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/')

    def test_catalog_filtering_and_search(self):
        """Test search query and brand filtering in home view."""
        # Search match
        response = self.client.get('/?q=Astrox')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yonex Astrox 100ZZ')

        # Search no match
        response = self.client.get('/?q=NonExistentGear')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No tournament equipment matched')

    def test_product_detail_page_loads_and_displays_specs(self):
        """Test product detail page displays technical badminton specs and stock."""
        response = self.client.get(reverse('product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yonex Astrox 100ZZ')
        self.assertContains(response, '4U/G5 • Extra Stiff • 28 LBS')
        self.assertContains(response, 'In Stock')

    def test_customer_can_post_review_when_logged_in(self):
        """Authenticated player can submit product review."""
        self.client.login(username='player_viktor', password='Password123!')
        response = self.client.post(
            reverse('product_detail', kwargs={'slug': self.product.slug}),
            {'rating': 5, 'comment': 'Best racquet ever produced. Unbeatable smash speed.'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Review.objects.filter(product=self.product, user=self.regular_user).exists())
        self.assertContains(response, 'Best racquet ever produced')

    def test_checkout_requires_login(self):
        """Guest cannot checkout directly without logging in first."""
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_full_checkout_flow_and_order_history(self):
        """Logged-in user checks out, decrements stock, and views order in My Orders & Invoice."""
        self.client.login(username='player_viktor', password='Password123!')
        cart_payload = json.dumps([{
            'name': self.product.name,
            'price': float(self.product.price),
            'qty': 2,
            'image': '/static/' + self.product.image_url
        }])

        post_data = {
            'full_name': 'Viktor Axelsen',
            'phone_number': '9876543210',
            'address': 'Kanteerava Indoor Stadium, Kasturba Road',
            'city': 'Bangalore',
            'state': 'Karnataka',
            'pincode': '560001',
            'payment_method': 'UPI',
            'cart_data': cart_payload
        }

        response = self.client.post(reverse('checkout'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ORDER CONFIRMED')

        # Verify Order created
        order = Order.objects.filter(user=self.regular_user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_amount, self.product.price * 2)

        # Verify stock decremented (10 - 2 = 8)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 8)

        # Verify order appears in My Orders page
        response_orders = self.client.get(reverse('my_orders'))
        self.assertEqual(response_orders.status_code, 200)
        self.assertContains(response_orders, order.order_id)
        self.assertContains(response_orders, 'Yonex Astrox 100ZZ')

        # Verify order appears in Invoice view
        response_invoice = self.client.get(reverse('order_detail', kwargs={'order_id': order.order_id}))
        self.assertEqual(response_invoice.status_code, 200)
        self.assertContains(response_invoice, f'INV-{order.order_id}')
        self.assertContains(response_invoice, 'BlueDart Apex Air')
