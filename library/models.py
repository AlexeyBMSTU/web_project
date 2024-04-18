from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions.datetime import Now
class QuestionManagerMy(models.Manager):
    def get_best_questions(self):
        return self.all().order_by('-published_at').order_by('--rating')
    
    def get_new_questions(self):
        return self.all().order_by('-published_at')
    
    def get_tag_questions(self):
        return self.filter(name='Browser')
    
    def get_one_questions(self):
        return self.all().order_by('-created_at')
# Create models here.

class AnswerManager(models.Model):
    def get_best(self):
        return self.filter().order_by('-published_at').order_by('--rating')

    def get_new(self):
        return self.filter().order_by('-published_at')
class QuestionInfoQuery:
    REALLY_HOT_QUESTION_RATING = 0
    LIMIT_HOT_QUESTION = 100
class QuestionManager(models.Manager):
    def get_hot(self,
                rating: int = QuestionInfoQuery.REALLY_HOT_QUESTION_RATING,
                limit: int = QuestionInfoQuery.LIMIT_HOT_QUESTION):
        return self.filter(rating__gte=rating).order_by('-rating')

    def get_new(self):
        return self.filter().order_by('-published_at')


    def get_tag_questions(cls, tag):
        return cls.filter(title="Tag"+tag+" ")
    
    def get_question_by_tag(cls, tag):
        return cls.filter(tags=tag)

    def get_one_questions(self):
        return self.all().order_by('-published_at', '-correct')
    
    def get_question_id(self,id):
        return self.filter(question_id=id)

    
class TagModel(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
class QuestionModel(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()

    tags = models.ManyToManyField(TagModel, related_name='questions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    n_answers = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    published_at = models.DateTimeField(db_default=Now())

    objects = QuestionManager()
    def __str__(self):
        return self.title
    
class AnswerModel(models.Model):
    text = models.TextField()

    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    rating = models.IntegerField(default=0)
    correct = models.CharField(max_length=100)
    published_at = models.DateTimeField(db_default=Now())

    objects = AnswerManager()

class AnswerLikeModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey(AnswerModel, on_delete=models.CASCADE, related_name="answer_likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'answer'], name='unique_answer_like'),
        ]



class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(null=True, blank=True)

class QuestionLikeModel(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes')
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='question_likes')

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['user', 'question'], name='unique_question_like'),
    #     ]


