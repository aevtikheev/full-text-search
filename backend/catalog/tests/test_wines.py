from rest_framework.test import APIClient, APITestCase

from catalog.models import Wine, WineSearchWord
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

        self.assertEqual(4, len(response_results))
        self.assertCountEqual([1, 2, 3, 4], [item['id'] for item in response_results])

    def test_can_filter_on_country(self):
        response = self.client.get('/api/v1/catalog/wines/?country=France')
        response_results = response.data['results']

        self.assertEqual(2, len(response_results))
        self.assertCountEqual([3, 4], [item['id'] for item in response_results])

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

    def test_search_results_returned_in_correct_order(self):
        response = self.client.get('/api/v1/catalog/wines/?query=Chardonnay')
        response_results = response.data['results']

        self.assertEqual(2, len(response_results))
        self.assertListEqual([3, 4], [item['id'] for item in response_results])

    def test_search_vector_populated_on_save(self):
        wine = Wine.objects.create(
            country='US',
            points=80,
            price=1.99,
            variety='Pinot Grigio',
            winery='Charles Shaw',
        )
        wine = Wine.objects.get(id=wine.id)
        self.assertEqual("'charl':3A 'grigio':2A 'pinot':1A 'shaw':4A", wine.search_vector)

    def test_description_highlights_matched_words(self):
        response = self.client.get('/api/v1/catalog/wines/?query=wine')
        response_results = response.data['results']

        self.assertEqual(
            'A delicious bottle of <mark>wine</mark>.',
            response_results[0]['description'],
        )

    def test_wine_search_words_populated_on_save(self):
        WineSearchWord.objects.all().delete()
        Wine.objects.create(
            country='US',
            description='A cheap, but inoffensive wine.',
            points=80,
            price=1.99,
            variety='Pinot Grigio',
            winery='Charles Shaw',
        )
        wine_search_words = WineSearchWord.objects.all().order_by('word')
        wine_search_word_values = wine_search_words.values_list('word', flat=True)
        self.assertListEqual(
            [
                'a',
                'but',
                'charles',
                'cheap',
                'inoffensive',
                'shaw',
                'wine',
            ],
            list(wine_search_word_values),
        )

    def test_suggests_words_for_spelling_mistakes(self):
        WineSearchWord.objects.bulk_create([
            WineSearchWord(word='pinot'),
            WineSearchWord(word='grigio'),
            WineSearchWord(word='noir'),
            WineSearchWord(word='merlot'),
        ])
        response = self.client.get('/api/v1/catalog/wine-search-words/?query=greegio')
        response_results = response.data['results']

        self.assertEqual(1, len(response_results))
        self.assertEqual('grigio', response_results[0]['word'])
