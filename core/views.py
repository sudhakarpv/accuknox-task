from rest_framework import generics, pagination, status, viewsets
from django.db.models import Q
from django.utils import timezone
from .models import (User, FriendRequest,)
from .serializers import (UserSignupSerializer,
                          UserSearchSerializer, FriendRequestSerializer, UserSerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .utils import request_count_limit
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase


# Create your views here.


class UserLoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email__iexact=email).first()

        if user and user.check_password(password):
            access_token = str(AccessToken.for_user(user))
            print(access_token)
            return Response({'status': 1,
                            'message': "Signed in successfully",
                             'token': access_token,
                             'email': email}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserSignupAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSignupSerializer

    def post(self, request):
        user_email = request.data.get("email")
        if User.objects.filter(email=user_email).exists():
            return Response({'status': 0, 'message': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserSignupSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'status': 1, 'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)


class ListAllUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserSearchPagination(pagination.PageNumberPagination):
    page_size = 10


class UserSearchAPIView(generics.ListAPIView):
    serializer_class = UserSearchSerializer
    pagination_class = UserSearchPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        search_keyword = self.request.query_params.get('search')
        print(search_keyword)
        if search_keyword:
            queryset = User.objects.filter(
                Q(email__iexact=search_keyword) | Q(name__icontains=search_keyword))
            return queryset.order_by('id')
        return User.objects.none()


class SendFriendRequestView(APIView):
    def post(self, request):
        from_user = request.user.id
        print("from_user", from_user)
        to_user_id = request.data.get('to_user_id')

        if not to_user_id:
            return Response({'status': 0, 'message': 'To user id is required'}, status=status.HTTP_400_BAD_REQUEST)

        if request_count_limit(from_user):
            try:
                to_user = User.objects.get(id=to_user_id)
            except User.DoesNotExist:
                return Response({'status': 0, 'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            FriendRequest.objects.create(
                from_user_id=from_user, to_user_id=to_user.id)
            return Response({'status': 1, 'message': 'Friend request sent successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 0, 'message': 'You have reached the limit for sending friend requests. Try after 1 minute'},
                            status=status.HTTP_400_BAD_REQUEST)


class UpdateFriendRequestView(APIView):
    def put(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(id=pk, accepted=False)
        except FriendRequest.DoesNotExist:
            return Response({'status': 0, 'message': 'Friend request does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        action = request.data.get('action')
        if action == 'accept':
            friend_request.accepted = True
        elif action == 'reject':
            friend_request.rejected = True
        else:
            return Response({'status': 0, 'message': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.save()
        return Response({'status': 1, 'message': f'Friend request {action} successfully'}, status=status.HTTP_200_OK)


class ListFriendsView(APIView):
    def get(self, request):
        user = request.user.id
        q_friends = FriendRequest.objects.filter(
            from_user_id=user, accepted=True)
        friends = [dict(name=f_request.to_user.name,
                        created_at=f_request.created_at) for f_request in q_friends]
        return Response({'status': 1, 'message': 'Fetched', 'data': friends}, status=status.HTTP_200_OK)


class ListPendingRequestsView(APIView):
    def get(self, request):
        user = request.user.id
        q_pending_requests = FriendRequest.objects.filter(to_user=user,
                                                          accepted=False, rejected=False)
        pending_request = [dict(id=f_request.id, request_message=f'your have friend request from {f_request.from_user.name}',
                                created_at=f_request.created_at) for f_request in q_pending_requests]
        return Response({'status': 1, 'message': 'Fetched', 'data': pending_request}, status=status.HTTP_200_OK)
