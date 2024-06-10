from rest_framework.routers import DefaultRouter
from chat.viewsets import ChatRoomViewSets

router = DefaultRouter()
router.register('chatroom', ChatRoomViewSets, basename='chatroom')
urlpatterns = router.urls