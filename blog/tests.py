from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from .models import Post

class BlogViewTests(TestCase):
    fixtures = ['db.json']

    def test_post_list_not_empty(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response=response, text="Lorem ipsum")

    def test_get_detail(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response=response, text="Lorem ipsum")

    def test_new_post_get(self):
        self.assertEqual(Post.objects.count(), 5)
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 5)

    def test_new_post_create_ok(self):
        response = self.client.post('/admin/login/', {'username': "admin", 'password': "1234567admin"})
        # self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 5)

        response = self.client.post(reverse('post_new'), {'title':'test title', 'text':'new test post'})
        # self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 6)

        response = self.client.get(reverse('post_detail', kwargs={'pk':6}))
        self.assertContains(response=response, text='test title')
        self.assertContains(response=response, text='test post')  

    def test_edit_post_change_post_ok(self):

        response = self.client.post('/admin/login/', {'username': "admin", 'password': "1234567admin"})
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('post_edit', kwargs={'pk':3}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('post_edit', kwargs={'pk':3}), {'title':'edit title', 'text':'edit post'})
        response = self.client.get(reverse('post_detail', kwargs={'pk':3}))
        self.assertContains(response=response, text='edit title')
        self.assertContains(response=response, text='edit post')  

         



