from rest_framework.test import APIClient, APITestCase

from catalog.models import Wine
from catalog.serializers import WineSerializer


class ViewTests(APITestCase):
    fixtures = ['test_wines.json']

    def setUp(self):
        self.client = APIClient()

    def test_empty_query_returns_everything(self):
        response = self.client.get('/api/v1/catalog/wines/')
        response_results = response.data['results']

        wines = Wine.objects.all()
        self.assertEqual(response_results, WineSerializer(wines, many=True).data)

    def test_query_matches_variety(self):
        response = self.client.get('/api/v1/catalog/wines/?query=Cabernet')
        response_results = response.data['results']

        self.assertEqual(1, len(response_results))
        self.assertEqual(1, response_results[0]['id'])

    def test_query_matches_winery(self):
        response = self.client.get('/api/v1/catalog/wines/?query=Barnard')
        response_results = response.data['results']

        self.assertEqual(1, len(response_results))
        self.assertEqual(2, response_results[0]['id'])

    def test_query_matches_description(self):
        response = self.client.get('/api/v1/catalog/wines/?query=wine')
        response_results = response.data['results']

        self.assertEqual(3, len(response_results))
        self.assertCountEqual([1, 2, 3], [item['id'] for item in response_results])

    def test_can_filter_on_country(self):
        response = self.client.get('/api/v1/catalog/wines/?country=France')
        response_results = response.data['results']

        self.assertEqual(1, len(response_results))
        self.assertEqual(3, response_results[0]['id'])

    def test_can_filter_on_points(self):
        response = self.client.get('/api/v1/catalog/wines/?points=87')
        response_results = response.data['results']

        self.assertEqual(1, len(response_results))
        self.assertEqual(2, response_results[0]['id'])

    def test_country_must_be_exact_match(self):
        response = self.client.get('/api/v1/catalog/wines/?country=Frances')
        response_results = response.data['results']

        self.assertEqual(0, len(response_results))
        self.assertEqual(response_results, [])
