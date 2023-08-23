from django.contrib.messages import get_messages
from django.test import TestCase


class TestViews(TestCase):
    def setUp(self) -> None:
        self.url = 'http://localhost:8000'

    def test_render_main_page_with_category_id(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('main.html')

    def test_dont_create_question(self):
        question = {'test': 'test', 'title': 'test', 'category': 1}

        response = self.client.post('/create_question', data=question, user=1)
        messages = list(get_messages(response.wsgi_request))

        print(messages[0], 'are messages')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(messages), 1)