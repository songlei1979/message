from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ChatRoom
from .serializers import ChatRoomSerializer
from django.urls import reverse


class ChatRoomViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.chatroom1 = ChatRoom.objects.create(name='Test Room 1')
        cls.chatroom2 = ChatRoom.objects.create(name='Test Room 2')

    def setUp(self):
        self.client = APIClient()

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
