from django.urls import path
from .views import *


urlpatterns = [
    path('signup', UserSignupAPIView.as_view(), name='signup'),
    path('signin', UserLoginAPIView.as_view(), name='signin'),
    path('list-all-users', ListAllUser.as_view(), name='list-all-users'),
    path('search-user', UserSearchAPIView.as_view(), name='search-user'),
    path('send-friend-request', SendFriendRequestView.as_view(),
         name='send-friend-request'),
    path('update-friend-request/<int:pk>', UpdateFriendRequestView.as_view(),
         name='update-friend-request'),
    path('list-friends', ListFriendsView.as_view(), name='list-friends'),
    path('pending-friend-request', ListPendingRequestsView.as_view(),
         name='pending-friend-request')
]
