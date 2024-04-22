from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from rest_framework_simplejwt.tokens import Token, AccessToken, RefreshToken
from rest_framework_simplejwt.utils import get_md5_hash_password
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.shortcuts import get_object_or_404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .permissions import IsGetOrIsAuthenticated
from .serializers import *
from .models import *

from time import perf_counter 
from django.core.handlers.wsgi import WSGIRequest

class Signup(APIView):
    # username, email, display_name
    def post(self, request: WSGIRequest, format=None):
        data = request.data

        user_serializer = UserSerializer(data=data)
        if user_serializer.is_valid():
            user_profile_serializer = UserProfileSerializer(data=data)
            if user_profile_serializer.is_valid():
                user = user_serializer.save()
                user.set_password(data['password'])
                user.save()
                user_profile_serializer.save(user=user)
                refresh = RefreshToken.for_user(user)

                data = {
                    "refresh":str(refresh),
                    "access":str(refresh.access_token),
                    "user": user_serializer.data,
                }
                return Response(data=data, status=status.HTTP_201_CREATED)
            return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Login(APIView):
    def post(self, request: WSGIRequest, format=None):
        data = request.data
        user = get_object_or_404(User, username=data['username'])
        if not user.check_password(data['password']):
            return Response({"detail":"Wrong password."}, status=status.HTTP_401_UNAUTHORIZED)
        
        tokens = RefreshToken().for_user(user)
        tokens_obj = {
            "refresh": str(tokens),
            "access": str(tokens.access_token),
        }

        return Response({"detail":"approved", "refresh":tokens_obj}, status=status.HTTP_200_OK)

###


class QuestionView(APIView):
    permission_classes = [IsGetOrIsAuthenticated]

    # title, content
    def post(self, request: WSGIRequest, format=None):
        user = request.user
        data = request.data
        question_serializer = QuestionSerializer(data=data)
        if question_serializer.is_valid():
            question_serializer.save(user=user)
            return Response({"detail":"approved", "question":question_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request: WSGIRequest, pk, format=None):
        question = get_object_or_404(Question, pk=pk)
        question_serializer = QuestionSerializer(question)
        
        return Response({"detail":"approved", "question":question_serializer.data}, status=status.HTTP_200_OK)
    
class AnswerView(APIView):
    permission_classes = [IsGetOrIsAuthenticated]

    # title, content
    def post(self, request: WSGIRequest, format=None):
        user = request.user
        data = request.data
        answer_serializer = AnswerSerializer(data=data)
        if answer_serializer.is_valid():
            question = get_object_or_404(Question, id=data["question_id"])
            answer_serializer.save(user=user, question=question)
            return Response({"detail":"approved", "answer":answer_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request: WSGIRequest, pk, format=None):
        answer = get_object_or_404(Answer, pk=pk)
        answer_serializer = AnswerSerializer(answer)
        
        return Response({"detail":"approved", "answer":answer_serializer.data}, status=status.HTTP_200_OK)

class CommentView(APIView):
    permission_classes = [IsGetOrIsAuthenticated]

    # content, question_id or answer_id
    def post(self, request: WSGIRequest, format=None):
        user = request.user
        data: dict = request.data
        comment_serializer = CommentSerializer(data=data)
        if comment_serializer.is_valid():
            if data.get("question_id", False):
                question = get_object_or_404(Question, id=data["question_id"])
                comment_serializer.save(user=user, question=question)
            if data.get("answer_id", False):
                answer = get_object_or_404(Answer, id=data["answer_id"])
                comment_serializer.save(user=user, answer=answer)

            return Response({"detail":"approved", "comment":comment_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request: WSGIRequest, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        comment_serializer = CommentSerializer(comment)
        
        return Response({"detail":"approved", "answer":comment_serializer.data}, status=status.HTTP_200_OK)