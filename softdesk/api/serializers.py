from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Contributor, Issue, Comment, UserProfile


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField()
    can_be_contacted = serializers.BooleanField()
    can_data_be_shared = serializers.BooleanField()

    class Meta:
        model = User
        fields = ["username", "password", "birth_date", "can_be_contacted", "can_data_be_shared"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        UserProfile.objects.create(
            user=user,
            birth_date=validated_data["birth_date"],
            can_be_contacted=validated_data["can_be_contacted"],
            can_data_be_shared=validated_data["can_data_be_shared"],
        )
        return user
