from django.contrib.auth.models import User
from django.db import models
from django.core.management.base import BaseCommand, CommandParser
# Register your models here.
# from  library.models import  User1, Answer, Question, Tag, FeedBack
from  library.models import QuestionManager, AnswerLikeModel, TagModel, QuestionModel, AnswerModel, ProfileModel, QuestionLikeModel, QuestionInfoQuery
from random import random, randint
from math import floor
import time
import sys
from datetime import datetime
from django.contrib.auth.models import User

from random import choice

class Command(BaseCommand):
    help = 'This command fills the database'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--ratio', type=int, default=10000, required=False,
                            help='The number of users to be created')
   
    def handle(self, *args, **options):
        print(options['ratio'])
        ratio = options.get('ratio', 0)
        
        self.__create_tags(ratio)
        #print("Tags created")
        self.stdout.write(self.style.SUCCESS('Tags created'))

        self.__create_users(ratio)
        #print("Users created")
        self.stdout.write(self.style.SUCCESS('Users created'))

        self.__create_questions(ratio)
        #print("Questions created")
        self.stdout.write(self.style.SUCCESS('Questions created'))

        self.__create_answers(ratio)
        #print("Answers created")
        self.stdout.write(self.style.SUCCESS('Answers created'))

        self.__create_likes_questions(100 * ratio)
        #print("Likes questions created")
        self.stdout.write(self.style.SUCCESS('Likes for questions created'))

        self.__create_likes_answers(100 * ratio)
        #print("Likes answers created")
        self.stdout.write(self.style.SUCCESS('Likes for answers created'))

        self.__add_tags_for_questions()
        #print("Tags and questions joined")
        self.stdout.write(self.style.SUCCESS('Tags -> questions '))


    @staticmethod
    def __create_tags(n_tags: int):
        tag1 = 'Browser'
        tag2 = 'Help'
        tag3 = 'Fix'
        tags_id = [tag1, tag2, tag3]
        new_tags = [
            TagModel(title=f'Tag{i} ')
            for i in range(n_tags)
        ]
        tages = TagModel.objects.bulk_create(new_tags)

    @staticmethod
    def __create_users(n_users: int):
        new_users = []
        for i in range(n_users):
            temp_user = User(
                username=f'User {i}',
            )
            new_users.append(temp_user)

        User.objects.bulk_create(new_users)

    @staticmethod
    def __create_questions(n_questions: int):
        text_question = 'Guys, please help me open the browser. Nothing helps...'
        title_question = 'How to open the browser?'
        users = User.objects.all()
        new_questions = []
        for i in range(n_questions):
            temp_question = QuestionModel(
                title=title_question + f'{ i} time',
                text=text_question + f'{ i} time',
                user=users[i % len(users)],
                rating = randint(0, 100000),
                
            )
            new_questions.append(temp_question)
        QuestionModel.objects.bulk_create(new_questions)

    @staticmethod
    def __create_answers(n_answers: int):
        text_answers = 'Error #404 indicates that the client was unable to access the server. This problem is with you, not the server. I know that to do. Try restarting the router. See if the domain name is spelled correctly.'
       
        users = User.objects.all()
        questions = QuestionModel.objects.all()
        new_answers = []
        corrects=["OK", " "]
        for i in range(n_answers):
            temp_answer = AnswerModel(
                text=text_answers + f'{ i} time',
                question=questions[i % len(questions)],
                user=users[i % len(users)],
                rating = randint(0, 100),
                correct = corrects[randint(0,1)],
            )
            new_answers.append(temp_answer)

        AnswerModel.objects.bulk_create(new_answers)

    @staticmethod
    def __create_likes_questions(n_likes: int):
        users = User.objects.all()
        questions = QuestionModel.objects.all()
        pair_user_question = set()
        n_tries = 0
        while len(pair_user_question) < n_likes and n_tries <= n_likes:
            n_tries += 1
            pair_user_question.add((choice(users), choice(questions)))

        new_likes = []
        for pair in pair_user_question:
            temp_like = QuestionLikeModel(
                user=pair[0],
                question=pair[1],
            )
            new_likes.append(temp_like)
        QuestionLikeModel.objects.bulk_create(new_likes)

    @staticmethod
    def __create_likes_answers(n_likes: int):
        users = User.objects.all()
        answers = AnswerModel.objects.all()
        pair_user_answer = set()
        n_tries = 0
        while len(pair_user_answer) < n_likes and n_tries < n_likes:
            n_tries += 1
            pair_user_answer.add((choice(users), choice(answers)))

        new_likes = []
        for pair in pair_user_answer:
            temp_like = AnswerLikeModel(
                user=pair[0],
                answer=pair[1],
            )
            new_likes.append(temp_like)
        AnswerLikeModel.objects.bulk_create(new_likes)

    @staticmethod
    def __add_tags_for_questions():
        questions = QuestionModel.objects.all()
        tags = TagModel.objects.all()
        for i in range(tags.count()):
            temp_tag = tags[i]
            temp_tag.questions.add(*questions[(i % len(questions)):(i + 5) % len(questions)])




