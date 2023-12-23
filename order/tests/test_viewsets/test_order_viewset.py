import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from product.models import Product
from order.factories import OrderFactory, UserFactory
from order.models import Order


class TestOrdeViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100, category=[self.category]
        )
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # import pdb; pdb.set_trace()

        order_data = json.loads(response.content)
        self.assertEqual(
            order_data["results"][0]["products"][0]["title"], self.product.title
        )
        self.assertEqual(
            order_data["results"][0]["products"][0]["price"], self.product.price
        )
        self.assertEqual(
            order_data["results"][0]["products"][0]["active"], self.product.active
        )
        self.assertEqual(
            order_data["results"][0]["products"][0]["category"][0]["title"],
            self.category.title,
        )

    def test_create_order(self):
        user = UserFactory()
        product1 = ProductFactory()
        product2 = ProductFactory()
        data = json.dumps({"products_id": [product1.id, product2.id], "user": user.id})

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=user)
