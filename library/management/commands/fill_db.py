from django.contrib.auth.models import User
from django.db import models
from django.core.management.base import BaseCommand, CommandParser
# Register your models here.
# from  library.models import  User1, Answer, Question, Tag, FeedBack
from  library.models import QuestionManager, AnswerLikeModel, TagModel, QuestionModel, AnswerModel, ProfileModel, QuestionLikeModel
from random import random, randint, shuffle
from math import floor
import time
import sys
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import time
from tqdm import tqdm
from random import choice
import random
from random import sample
from django.db import transaction
from django.db.models import Count


class Command(BaseCommand):
    help = 'This command fills the database'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--ratio', type=int, default=10, required=False,
                            help='The number of users to be created')
   
    def handle(self, *args, **options):
        print(options['ratio'])
        ratio = options.get('ratio', 0)

        print("Tag...")
        self.__create_tags(ratio)
        #print("Tags created")
        self.stdout.write(self.style.SUCCESS('Tags created'))

        print("User...")
        self.__create_users(ratio)
        #print("Users created")
        self.stdout.write(self.style.SUCCESS('Users created'))

        print("Profile...")
        self.__create_profile(ratio)
        #print("Profiles created")
        self.stdout.write(self.style.SUCCESS('Profiles created'))

        print("Qeestions...")
        self.__create_questions(10*ratio)
        #print("Questions created")
        self.stdout.write(self.style.SUCCESS('Questions created'))

        print("Answer...")
        self.__create_answers(100*ratio)
        #print("Answers created")
        self.stdout.write(self.style.SUCCESS('Answers created'))

        print("LikesQuestion...")
        self.__create_likes_questions(200 * ratio)
        #print("Likes questions created")
        self.stdout.write(self.style.SUCCESS('Likes for questions created'))

        print("LikesAnswer...")
        self.__create_likes_answers(200 * ratio)
        #print("Likes answers created")
        self.stdout.write(self.style.SUCCESS('Likes for answers created'))

        print("Tags->questions...")
        self.__add_tags_for_questions()
        #print("Tags and questions joined")
        self.stdout.write(self.style.SUCCESS('Tags -> questions '))

    
    @staticmethod
    def __create_tags(n_tags: int):

        new_tags = [
            TagModel(id = i,title=f'Tag{i}')
            for i in range(n_tags)
        ]
        tages = TagModel.objects.bulk_create(new_tags)
    
    @staticmethod
    def __create_users(n_users: int):
        new_users = []
        for i in tqdm(range(n_users)):
            arg = i
            temp_user = User(
                username=f'User {i}',
                password=make_password(f'aaaaaaa{i}{i}{i}')
            )

            new_users.append(temp_user)

        User.objects.bulk_create(new_users) 
       
    @staticmethod
    def __create_profile(n_profiles: int):
        new_profiles = []
        emails = ['gmail.com', 'yandex.ru', 'bk.ru']
        profiles = User.objects.all()
        for i in tqdm(range(n_profiles)):
            temp_profile = ProfileModel(
                user=profiles[i % len(profiles)],
                user_name = f'User {i % len(profiles)}',
                email = f'user{i}@{emails[i % len(emails)]}',
            )
            new_profiles.append(temp_profile)

        ProfileModel.objects.bulk_create(new_profiles)

    @staticmethod
    def __create_questions(n_questions: int):
        text_question = 'Guys, please help me open the browser. Nothing helps...'
        title_question = 'How to open the browser?'
        users = User.objects.all()
        tags = TagModel.objects.all()  # Предполагаем, что у вас есть модель Tag для хранения тегов
        new_questions = []

        for i in tqdm(range(n_questions)):
            temp_tags = sample(list(tags), 3)  # Выбор случайного набора тегов
            #print(temp_tags)
            temp_question = QuestionModel(
                title=title_question + f'{i} time',
                text=text_question + f'{i} time',
                user=users[i % len(users)],
                rating=randint(0, len(users)),
            )
            new_questions.append(temp_question)

        QuestionModel.objects.bulk_create(new_questions)

    @staticmethod
    def __create_answers(n_answers: int):
        text_answers = 'Error #404 indicates that the client was unable to access the server. This problem is with you, not the server. I know that to do. Try restarting the router. See if the domain name is spelled correctly.'
       
        users = User.objects.all()
        questions = QuestionModel.objects.all()
        all_ques = list( QuestionModel.objects.all() )
        new_answers = []
        corrects=["OK", " "]
        for i in tqdm(range(n_answers)):
            random_ques = random.choice(all_ques)
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
        tags = TagModel.objects.all()  # Предполагаем, что у вас есть модель Tag для хранения тегов
        
        for question in questions:       
            # Выбираем случайные теги, чтобы добавить к вопросу
            temp_tags = sample(list(tags), randint(1,3))  # Выбор случайного набора тегов
            question.tags.set(temp_tags)     


