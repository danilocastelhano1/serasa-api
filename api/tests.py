from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Productor


class ProductorIntegrationTestCase(APITestCase):
    def setUp(self):
        self.productor_url = reverse("productor-list")
        self.payload = {
            "cpf_cnpj": "228.547.730-98",
            "name": "João da Silva",
            "farm": {"name": "Fazenda Boa Esperança do Sul"},
            "city": "Sorriso",
            "state": "MT",
            "total_area": 1000.5,
            "agricultural_area": 800.0,
            "vegetation_area": 200.5,
            "seasons": [
                {"year": 2021, "cultures": [{"name": "Soja"}, {"name": "Milho"}]},
                {"year": 2022, "cultures": [{"name": "Café"}]},
            ],
        }

    def test_create_productor_successfully(self):
        """
        Creates a productor with a valid payload successfully
        """
        response = self.client.post(self.productor_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Productor.objects.count(), 1)
        value: str = "".join(v for v in self.payload["cpf_cnpj"] if v.isdigit())
        self.assertEqual(Productor.objects.first().cpf_cnpj, value)

    def test_create_productor_invalid_cnpj(self):
        """
        Not Creates a productor with a wrong cnpj
        """
        # given
        self.payload["cpf_cnpj"] = "57.862.994/0001-73"
        # when
        response = self.client.post(self.productor_url, self.payload, format="json")
        # then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid CNPJ.", response.content.decode("utf-8"))

    def test_create_productor_invalid_cpf(self):
        """
        Not Creates a productor with a wrong cpf
        """
        # given
        self.payload["cpf_cnpj"] = "065.457.710-28"
        # when
        response = self.client.post(self.productor_url, self.payload, format="json")
        # then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid CPF.", response.content.decode("utf-8"))

    def test_create_productor_existing_cpf_cnpj(self):
        """
        Not Creates a productor with a wrong cpf
        """
        # given
        self.payload["cpf_cnpj"] = "594.249.840-73"
        # when
        response = self.client.post(self.productor_url, self.payload, format="json")
        # then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # when
        response = self.client.post(self.productor_url, self.payload, format="json")
        # then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("CPF or CNPJ Already exists.", response.content.decode("utf-8"))

    def test_validates_total_area(self):
        """
        Not Creates a productor with a wrong cpf
        """
        # given
        self.payload["total_area"] = 100
        self.payload["agricultural_area"] = 200
        self.payload["vegetation_area"] = 400.5
        # when
        response = self.client.post(self.productor_url, self.payload, format="json")
        # then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "The sum of the 'agricultural_area' and 'vegetation_area' areas cannot exceed the total_area.",
            response.content.decode("utf-8"),
        )
