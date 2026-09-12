from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Organization, Shop

User = get_user_model()

class ShopAPITestCase(TestCase):


    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        self.organization = Organization.objects.create(
            name="Test Organization",
            description="Test description",
        )

        self.shop = Shop.objects.create(
            organization=self.organization,
            name="Test Shop",
            description="Test shop description",
            address="Test address",
            index=12345,
            is_deleted=False,
        )

        self.deleted_shop = Shop.objects.create(
            organization=self.organization,
            name="Deleted Shop",
            description="Deleted shop description",
            address="Deleted address",
            index=54321,
            is_deleted=True,
        )

        self.client = APIClient()

    def test_organizations_require_authentication(self):
        response = self.client.get("/api/organizations/")

        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_can_get_organizations(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/organizations/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        organization = response.data[0]

        self.assertEqual(
            organization["name"],
            "Test Organization",
        )

        self.assertEqual(
            organization["description"],
            "Test description",
        )

    def test_deleted_shop_is_not_returned(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/organizations/")

        self.assertEqual(response.status_code, 200)

        shops = response.data[0]["shops"]

        shop_names = [shop["name"] for shop in shops]

        self.assertIn("Test Shop", shop_names)
        self.assertNotIn("Deleted Shop", shop_names)

    def test_shop_put_updates_shop(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "name": "Updated Shop",
            "description": "Updated description",
            "address": "Updated address",
            "index": 99999,
        }

        response = self.client.put(
            f"/api/shops/{self.shop.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.shop.refresh_from_db()

        self.assertEqual(self.shop.name, "Updated Shop")
        self.assertEqual(
            self.shop.description,
            "Updated description",
        )
        self.assertEqual(
            self.shop.address,
            "Updated address",
        )
        self.assertEqual(self.shop.index, 99999)

    def test_shop_put_requires_index(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "name": "Updated Shop",
            "description": "Updated description",
            "address": "Updated address",
        }

        response = self.client.put(
            f"/api/shops/{self.shop.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("index", response.data)

    def test_shop_put_requires_authentication(self):
        data = {
            "name": "Updated Shop",
            "description": "Updated description",
            "address": "Updated address",
            "index": 99999,
        }

        response = self.client.put(
            f"/api/shops/{self.shop.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_shop_put_returns_404_for_missing_shop(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "name": "Updated Shop",
            "description": "Updated description",
            "address": "Updated address",
            "index": 99999,
        }

        response = self.client.put(
            "/api/shops/99999/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 404)

