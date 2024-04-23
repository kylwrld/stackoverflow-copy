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

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['vote']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'created_at', 'updated_at']
        read_only_fields = ('user',)

class AnswerSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Answer
        fields = ['id', 'content', 'n_votes', 'created_at', 'updated_at', 'user', 'comments']
        read_only_fields = ('user',)

    def to_representation(self, instance):
        data = super(AnswerSerializer, self).to_representation(instance)
        if data.get("comments", False):
            data["answer_comments"] = data.pop("comments")

        return data

class QuestionSerializer(serializers.ModelSerializer):    
    answers = AnswerSerializer(read_only=True, many=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'content', 'n_votes', 'created_at', 'updated_at', 'user', 'answers', 'comments']
        read_only_fields = ('user', 'votes')

    def to_representation(self, instance):
        data = super(QuestionSerializer, self).to_representation(instance)
        if data.get("comments", False):
            data["question_comments"] = data.pop("comments")
        
        return data
    
class BookmarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ["user", "question", "answer", "created_at"]
        read_only_fields = ("user",)