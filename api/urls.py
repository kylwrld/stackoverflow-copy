from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/signup/', views.Signup.as_view(), name='signup'),
    path('api/login/', views.Login.as_view(), name='login'),
    path('api/question/', views.QuestionView.as_view(), name='question'),
    path('api/question/<int:pk>/', views.QuestionView.as_view(), name='question_pk'),
    path('api/answer/', views.AnswerView.as_view(), name='answer'),
    path('api/answer/<int:pk>/', views.AnswerView.as_view(), name='answer_pk'),
    path('api/comment/', views.CommentView.as_view(), name='comment'),
    path('api/comment/<int:pk>/', views.CommentView.as_view(), name='comment_pk'),

    
    path("api/token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='token_refresh')

]
