from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions.datetime import Now
from django.db.models import Count
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
    def get_answer_with_id(self, answer_id):
        return self.filter(question = answer_id).order_by('-correct', '-published_at')

class QuestionManager(models.Manager):

    def get_hot(self):
        return self.order_by( '-rating', '-published_at')

    def get_new(self):
        return self.filter().order_by('-published_at')
    
    def get_question_by_id(self, question_id):
        return self.filter( id=question_id).annotate(num_tags=Count('tags'))
    
    def get_question_by_tag( self, tag_id ):
        return self.filter( tags = tag_id).annotate(num_tags=Count('tags'))
    
    def get_author_with_id(self, author_id):
        return self.filter(id = author_id)
    
    def get_all_users(self):
        return self.all()
    

class TagManager( models.Model ):
    def get_popular_tag( self ):
        return self.annotate(num_tags=Count('tags')).order_by('-rating')[:2]
    
    def get_new_question_list( self ):
        return self.all().annotate(num_tags=Count('tags')).order_by('-published_at')
    
    def get_best_question_list( self ):
        return self.all().annotate(num_tags=Count('tags')).order_by('-rating')
    

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
    user_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    def __str__(self):
        return self.email

class QuestionLikeModel(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes')
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='question_likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'question'], name='unique_question_like'),
        ]


