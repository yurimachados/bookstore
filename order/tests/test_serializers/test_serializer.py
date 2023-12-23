from django.test import TestCase
from order.tests.test_serializers.test_serializer import OrderFactory, UserFactory
from product.models import Product

# Create your tests here.


class OrderFactoryTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product1 = Product.objects.create(name="Product 1", price=10.0)
        self.product2 = Product.objects.create(name="Product 2", price=20.0)

    def test_order_creation(self):
        order = OrderFactory.create(
            user=self.user, products=[self.product1, self.product2]
        )
        self.assertEqual(order.user, self.user)
        self.assertIn(self.product1, order.products.all())
        self.assertIn(self.product2, order.products.all())
