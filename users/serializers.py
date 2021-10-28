from rest_framework import serializers

from users.models import Client, Match


class ClientRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='Повторите пароль')

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'sex', 'avatar', 'password', 'password2']

    def save(self, *args, **kwargs):
        client = Client(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            sex=self.validated_data['sex'],
            avatar=self.validated_data['avatar'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError("Пароли не совпадают")
        client.set_password(password)
        client.save()
        return client


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'sex', 'from_match', 'to_match']


class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = ['to_match', ]
