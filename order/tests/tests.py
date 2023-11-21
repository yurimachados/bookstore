from django.test import TestCase
from order.tests.factories import OrderFactory, UserFactory
from product.tests.factories import ProductFactory

class OrderFactoryTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.product1 = ProductFactory.create()
        self.product2 = ProductFactory.create()

    def test_order_creation(self):
        order = OrderFactory.create(user=self.user, products=[self.product1, self.product2])
        self.assertEqual(order.user, self.user)
        self.assertIn(self.product1, order.products.all())
        self.assertIn(self.product2, order.products.all())
