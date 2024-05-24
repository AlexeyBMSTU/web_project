from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions.datetime import Now
from django.db.models import Count

# Create models here.

class AnswerManager( models.Manager ):
    def get_answer_with_id( self, answer_id ):
        return self.filter( question = answer_id ).order_by('-correct', '-published_at')

class QuestionManager( models.Manager ):

    def get_new_question_list( self ):
        return self.all().annotate(num_tags=Count('tags')).order_by('-published_at')
    
    def get_best_question_list( self ):
        return self.all().annotate(num_tags=Count('tags')).order_by('-rating', '-published_at')
    
    def get_question_by_id(self, question_id):
        return self.filter( id=question_id).annotate(num_tags=Count('tags'))
    
    def get_question_by_tag( self, tag_id ):
        return self.filter( tags = tag_id ).annotate(num_tags=Count('tags'))
    

class TagManager( models.Manager ):
    def get_popular_tag( self ):
        return self.annotate(num_questions=Count('questions')).order_by('-num_questions')[:10]
    def get_current_tag( self, tag_id ):
        return self.filter( id = tag_id )
        
         
        

class TagModel( models.Model ):
    title = models.CharField(max_length=100)
    
    objects = TagManager()
     
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

    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='question')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    rating = models.IntegerField(default=0)
    correct = models.CharField(max_length=100)
    published_at = models.DateTimeField(db_default=Now())

    objects = AnswerManager()

class AnswerLikeModel(models.Model):
    statusChoice = [{0, "None"}, {1, "Like"}]
    status = models.IntegerField(choices=statusChoice, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey(AnswerModel, on_delete=models.CASCADE, related_name="answer_likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'answer'], name='unique_answer_like'),
        ]




class QuestionLikeModel(models.Model):
    statusChoice = [{0, "None"}, {1, "Like"}]
    status = models.IntegerField(choices=statusChoice, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes')
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='question_likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'question'], name='unique_question_like'),
        ]


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(null=True, blank=True)
    user_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    def __str__(self):
        return self.email
