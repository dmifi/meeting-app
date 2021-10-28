from django.http import Http404
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Client, Match
from users.serializers import ClientRegistrationSerializer, ClientSerializer, MatchSerializer


# Client Views
class RegistrationClientView(CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ClientRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class ClientListView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]


class ClientDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]


# Match Views
class MatchListView(ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class MatchDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [AllowAny]


class SetMatch(APIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [AllowAny]

    def check_mutuality(self, user_one, user_two):
        all_match = Match.objects.filter(from_match=user_two.id)
        for match in all_match:
            if match.to_match == user_one:
                return True

    def get_object_one(self, pk):
        try:
            return Match.objects.filter(from_match=pk)
        except Match.DoesNotExist:
            raise Http404

    def post(self, request, pk, *args, **kwargs):
        serializer = MatchSerializer(data=request.data)
        current_user = Client.objects.get(pk=pk)
        if serializer.is_valid() and serializer.validated_data['to_match'] != current_user:
            try:
                serializer.save(from_match=current_user)
            except IntegrityError:
                data = serializer.errors
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            to_match_user = Client.objects.get(pk=serializer.data["to_match"])
            if self.check_mutuality(current_user, to_match_user):
                message = {'message': f'У вас взаимная симпатия с пользователем {to_match_user}. '
                                      f'Его электронная почта: {to_match_user.email}. '
                                      f'Можете написать ему. '}
                return Response(message, status=status.HTTP_201_CREATED)
            data = {'response': True}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        match = self.get_object_one(pk)
        serializer = MatchSerializer(match, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        match = self.get_object(pk)
        match.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
