import django.contrib.admin 
from django.contrib import admin

# Register your models here.
# from .models  import User1, Answer, Question, Tag, FeedBack
from  library.models import QuestionManager, QuestionModel, AnswerLikeModel, TagModel, ProfileModel, QuestionLikeModel, AnswerModel

admin.site.register(QuestionModel)
admin.site.register(QuestionLikeModel)
admin.site.register(AnswerModel)
admin.site.register(AnswerLikeModel)
admin.site.register(TagModel)
admin.site.register(ProfileModel)

