from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from random import choices
from string import ascii_letters
from .models import Product


class IndexPageTest(TestCase):
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        response = self.client.post(
            reverse('eshop:product_create'),
            {
                "name": self.product_name,
                "price": 123.45,
                "description": "A good table",
                "discount": 10
            }
        )
        self.assertRedirects(response, reverse('eshop:product_list'))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.product = Product.objects.create(name="Best Product")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse('eshop:product_details'), kwargs={"pk": self.product.pk}
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse('eshop:product_details'), kwargs={"pk": self.product.pk}
        )
        self.assertContains(response, self.product.name)


class ProductListViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json'
    ]

    def test_products(self):
        response = self.client.get(reverse('eshop:products_list'))
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk
        )
        self.assertTemplateUsed(response, 'eshop:product_list')


class OrderListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects().create_user(username='bob_test', password='qwerty')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse('eshop:order_list'))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('eshop:order_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json'
    ]

    def test_get_products_view(self):
        response = self.client.get(reverse('eshop:product_export'))
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(products_data["products"], expected_data)
