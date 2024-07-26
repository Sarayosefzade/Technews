from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import NewsModel, Tag
from .serializers import NewsSerializer, TagSerializer

class TagModelTest(TestCase):
    def test_tag_creation(self):
        tag = Tag.objects.create(name='Technology')
        self.assertEqual(tag.name, 'Technology')

class NewsModelTest(TestCase):
    def setUp(self):
        self.tags = Tag.objects.create(name='Technology')
        self.news = NewsModel.objects.create(
            title='Test News',
            description='This is a test news description.',
            source='http://example.com'
        )
        self.news.tags.add(self.tags)

    def test_news_creation(self):
        self.assertEqual(self.news.title, 'Test News')
        self.assertEqual(self.news.description, 'This is a test news description.')
        self.assertEqual(self.news.source, 'http://example.com')
        self.assertIn(self.tags, self.news.tags.all())

class TagSerializerTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Technology')
        self.serializer = TagSerializer(instance=self.tag)

    def test_tag_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['name'], 'Technology')

class NewsSerializerTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Technology')
        self.news = NewsModel.objects.create(
            title='Test News',
            description='This is a test news description.',
            source='http://example.com'
        )
        self.news.tags.add(self.tag)
        self.serializer = NewsSerializer(instance=self.news)

    def test_news_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['title'], 'Test News')
        self.assertEqual(data['description'], 'This is a test news description.')
        self.assertEqual(data['source'], 'http://example.com')
        self.assertEqual(len(data['tags']), 1)
        self.assertEqual(data['tags'][0], self.tag.id)

class NewsAPITest(APITestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Technology')
        self.news = NewsModel.objects.create(
            title='Test News',
            description='This is a test news description.',
            source='http://example.com'
        )
        self.news.tags.add(self.tag)

    def test_get_news_list(self):
        url = reverse('newsmodel-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test News')

    def test_filter_news_by_tag(self):
        url = reverse('newsmodel-list')
        response = self.client.get(url, {'tags': 'Technology'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test News')

    def test_create_news(self):
        url = reverse('newsmodel-list')
        data = {
            'title': 'Another News',
            'description': 'This is another test news description.',
            'source': 'http://example2.com',
            'tags': [self.tag.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewsModel.objects.count(), 2)
        self.assertEqual(NewsModel.objects.get(id=2).title, 'Another News')
