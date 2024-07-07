from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Contributor, Issue, Comment, UserProfile
from django.db import transaction


class ProjectSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Project.
    """

    class Meta:
        model = Project
        fields = "__all__"


class ContributorSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Contributor.
    """

    class Meta:
        model = Contributor
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Issue.
    """

    class Meta:
        model = Issue
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Comment.
    """

    class Meta:
        model = Comment
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle UserProfile.
    """

    class Meta:
        model = UserProfile
        fields = ["birth_date", "can_be_contacted", "can_data_be_shared"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'enregistrement des utilisateurs.
    """

    birth_date = serializers.DateField(write_only=True)
    can_be_contacted = serializers.BooleanField(write_only=True)
    can_data_be_shared = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "birth_date", "can_be_contacted", "can_data_be_shared"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur et son profil associé.
        """
        birth_date = validated_data.pop("birth_date")
        can_be_contacted = validated_data.pop("can_be_contacted")
        can_data_be_shared = validated_data.pop("can_data_be_shared")

        user = User.objects.create_user(username=validated_data["username"], password=validated_data["password"])

        UserProfile.objects.create(
            user=user, birth_date=birth_date, can_be_contacted=can_be_contacted, can_data_be_shared=can_data_be_shared
        )

        return user
