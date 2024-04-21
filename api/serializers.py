from rest_framework import serializers
from .models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['display_name']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', "profile"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'content', 'created_at', 'updated_at', 'user']
        read_only_fields = ('user',)

class QuestionSerializer(serializers.ModelSerializer):    
    answers = AnswerSerializer(read_only=True, many=True)
    
    class Meta:
        model = Question
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'user', 'answers']
        read_only_fields = ('user',)