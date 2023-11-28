from django.test import TestCase
from product.models import Product, Category
from product.factories import ProductFactory, CategoryFactory

class CategoryTest(TestCase):
    def test_category_creation(self):
        category = CategoryFactory.create()
        self.assertTrue(isinstance(category, Category))
        self.assertTrue(category.active in [True, False])
    
    def test_category_title(self):
        category = CategoryFactory.create(title="Test Category")
        self.assertEqual(category.title, "Test Category")
    
    def test_category_slug(self):
        category = CategoryFactory.create(slug="Test Category")
        self.assertEqual(category.slug, "Test Category")
    
    def test_category_description(self):
        category = CategoryFactory.create(description="Test Description")
        self.assertEqual(category.description, "Test Description")
    
class ProductTest(TestCase):
    def test_product_creation(self):
        categories = [CategoryFactory(), CategoryFactory()]

        product = ProductFactory(category=categories)

        self.assertTrue(isinstance(product, Product))
        for category in product.category.all():
            self.assertTrue(isinstance(category, Category))
        self.assertIn(product.active, [True, False])

    def test_product_title(self):
        product = ProductFactory(title="Test Product")
        self.assertEqual(product.title, "Test Product")
    
    def test_product_price(self):
        product = ProductFactory.create(price=10.0)
        self.assertEqual(product.price, 10.0)
    
    def test_product_description(self):
        product = ProductFactory.create(description="Test Description")
        self.assertEqual(product.description, "Test Description")
