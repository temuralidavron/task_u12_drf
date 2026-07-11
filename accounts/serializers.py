from django.contrib.auth import get_user_model
# from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

# from projects.serializers import ProjectSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # project = ProjectSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
#
#
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, validators=[validate_password])
#     owned_projects=ProjectSerializer(read_only=True,many=True)
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name','owned_projects')
#
#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user
