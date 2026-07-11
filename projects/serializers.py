from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Project, Task
User = get_user_model()
from django.contrib.auth.password_validation import validate_password


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'owner', 'members')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'status', 'project', 'assignees', 'created_time')
        read_only_fields = ('created_time',)

    def validate_project(self, value):
        user = self.context['request'].user
        if value.owner_id != user.id and not value.members.filter(pk=user.pk).exists():
            raise serializers.ValidationError('You do not have access to this project.')
        return value




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    owned_projects=ProjectSerializer(read_only=True,many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name','owned_projects')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
