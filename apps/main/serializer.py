from rest_framework import serializers
from .models import MyUser, Publication, Comment
from django.contrib.auth import authenticate


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'username', 'avatar', 'description', 'is_staff']
        read_only_fields = ['id', 'is_staff']


class PublicationSerializer(serializers.ModelSerializer):
    author = MyUserSerializer(read_only=True)

    class Meta:
        model = Publication
        fields = ['id', 'title', 'p_type', 'author', 'text', 'file']
        read_only_fields = ['id']


class CommentSerializer(serializers.ModelSerializer):
    author = MyUserSerializer(read_only=True)
    publication = PublicationSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'publication', 'text']
        read_only_fields = ['id']


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'password', 'avatar']

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            avatar=validated_data.get('avatar', 'avatars/unknown.png'),
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")