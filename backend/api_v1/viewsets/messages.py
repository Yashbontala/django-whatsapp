from rest_framework import generics, viewsets
from rest_framework.response import Response
from ..serializers.messages import WhatsappChatSerializer, WhatsappMediaSerializer, FriendMessagesSerializer
from messages_app.models import WhatsappChatMessages, WhatsappMediaMessages, FriendMessages
from users_auth.permissions import HasWhatsappLoggedIn, HasAPIAccess
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class WhatsappChatAllViewset(generics.ListAPIView):
    queryset = WhatsappChatMessages.objects.all()
    serializer_class = WhatsappChatSerializer
    permission_classes = (HasAPIAccess, )

    def get_queryset(self):
        queryset = super(WhatsappChatAllViewset, self).get_queryset()
        queryset = queryset.filter(number__user__api_key__api_key=self.request.apikey)
        return queryset


class WhatsappChatViewset(generics.ListCreateAPIView):
    queryset = WhatsappChatMessages.objects.all()
    serializer_class = WhatsappChatSerializer
    lookup_field = 'pk'
    # detail = True
    permission_classes = (HasAPIAccess, )

    def get(self, request, pk):
        queryset = self.get_queryset().filter(
            number_id=pk, number__user__api_key__api_key=request.apikey
        ).order_by('-message_timestamp')
        serializer = WhatsappChatSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, pk):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, pk)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer, pk):
        serializer.save(number_id=pk, message_type='OUT')


class WhatsappChatDetailViewset(generics.RetrieveDestroyAPIView):
    queryset = WhatsappChatMessages.objects.all()
    serializer_class = WhatsappChatSerializer
    lookup_field = 'id'
    permission_classes = (HasAPIAccess, )

    def get_queryset(self):
        queryset = super(WhatsappChatDetailViewset, self).get_queryset()
        queryset = queryset.filter(number_id=self.kwargs['pk'], number__user__api_key__api_key=self.request.apikey)
        return queryset

class WhatsappMediaViewset(generics.ListCreateAPIView):
    queryset = WhatsappMediaMessages.objects.all()
    serializer_class = WhatsappMediaSerializer
    lookup_field = 'pk'
    permission_classes = (HasAPIAccess, )

    def get(self, request, pk):
        queryset = self.get_queryset().filter(
            number_id=pk, number__user__api_key__api_key=request.apikey
        ).order_by('-message_timestamp')
        serializer = WhatsappMediaSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, pk):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, pk)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer, pk):
        serializer.save(number_id=pk, message_type='OUT')


class WhastappMediaDetailViewset(generics.RetrieveDestroyAPIView):
    queryset = WhatsappMediaMessages.objects.all()
    serializer_class = WhatsappMediaSerializer
    lookup_field = 'id'
    permission_classes = (HasAPIAccess, )

    def get_queryset(self):
        queryset = super(WhastappMediaDetailViewset, self).get_queryset()
        queryset = queryset.filter(number_id=self.kwargs['pk'], number__user__api_key__api_key=self.request.apikey)
        return queryset


class FriendMessagesViewset(viewsets.ModelViewSet):
    queryset = FriendMessages.objects.all()
    serializer_class = FriendMessagesSerializer
    lookup_field = 'id'
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = super(FriendMessagesViewset, self).get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)