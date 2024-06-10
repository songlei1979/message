from rest_framework import viewsets
from chat.models import ChatRoom
from chat.serializers import ChatRoomSerializer


class ChatRoomViewSets(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer