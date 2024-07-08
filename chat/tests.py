from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ChatRoom
from .serializers import ChatRoomSerializer
from django.urls import reverse

from .views import sumNumbers


class ChatRoomViewSetTest(TestCase):
    @classmethod
    def setUpTestData(self):
        # Set up data for the whole TestCase
        self.chatroom1 = ChatRoom.objects.create(name='Test Room 1')
        self.chatroom2 = ChatRoom.objects.create(name='Test Room 2')

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_list_chatrooms(self):
        response = self.client.get(reverse('chatroom-list'))
        chatrooms = ChatRoom.objects.all()
        serializer = ChatRoomSerializer(chatrooms, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_chatroom(self):
        data = {'name': 'New Test Room'}
        response = self.client.post(reverse('chatroom-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatRoom.objects.count(), 3)
        self.assertEqual(ChatRoom.objects.get(id=response.data['id']).name, 'New Test Room')

    def test_retrieve_chatroom(self):
        response = self.client.get(reverse('chatroom-detail', kwargs={'pk': self.chatroom1.pk}))
        chatroom = ChatRoom.objects.get(pk=self.chatroom1.pk)
        serializer = ChatRoomSerializer(chatroom)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_chatroom(self):
        data = {'name': 'Updated Test Room'}
        response = self.client.put(reverse('chatroom-detail', kwargs={'pk': self.chatroom1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.chatroom1.refresh_from_db()
        self.assertEqual(self.chatroom1.name, 'Updated Test Room')

    def test_delete_chatroom(self):
        response = self.client.delete(reverse('chatroom-detail', kwargs={'pk': self.chatroom1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ChatRoom.objects.count(), 1)


class SumNumbersFunctionTest(TestCase):

    def test_positive_range(self):
        result = sumNumbers(1, 5)
        self.assertEqual(result, 15)

    def test_reverse_range(self):
        result = sumNumbers(5, 1)
        self.assertEqual(result, 15)

    def test_negative_range(self):
        result = sumNumbers(-3, 3)
        self.assertEqual(result, 0)

    def test_single_number(self):
        result = sumNumbers(5, 5)
        self.assertEqual(result, 5)

    def test_zero_range(self):
        result = sumNumbers(0, 0)
        self.assertEqual(result, 0)


class SumNumbersViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('sum_numbers')

    def test_sum_numbers(self):
        response = self.client.post(self.url, {'start_num': 1, 'end_num': 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 15)

    def test_sum_numbers_reverse_order(self):
        response = self.client.post(self.url, {'start_num': 5, 'end_num': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 15)

    def test_sum_numbers_negative(self):
        response = self.client.post(self.url, {'start_num': -3, 'end_num': 3}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 0)


