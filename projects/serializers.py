from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Project, Task


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
