from django.db import models
from django.contrib.auth.models import User

### User:

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Follow(models.Model):
    follow_account = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

###

### Questions, Answers and Comments:

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="questions")
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def n_votes(self):
        print(self)
        positive = Vote.objects.filter(question_id=self.id, vote=True).count()
        negative = Vote.objects.filter(question_id=self.id, vote=False).count()
        return positive - negative

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def n_votes(self):
        positive = Vote.objects.filter(answer_id=self.id, vote=True).count()
        negative = Vote.objects.filter(answer_id=self.id, vote=False).count()
        return positive - negative

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="comments")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

###

### Features:

    updated_at = models.DateTimeField(auto_now=True)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="votes")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="votes", null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes', null=True, blank=True)
    vote = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="bookmarks", null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="bookmarks", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)