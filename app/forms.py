from dataclasses import fields
from random import randint
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import CharField
from library.models import AnswerModel, ProfileModel, QuestionModel, TagModel
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.hashers import make_password
from django.forms.utils import ErrorList


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField( min_length=5, widget=forms.PasswordInput )

    def clean_password( self ):

        password_input = self.cleaned_data['password']
        user_input = self.cleaned_data['username']
        user_db = User.objects.filter( username = user_input)
        if str(*user_db) != "":
            user_get = User.objects.get( username = user_input)
            if user_get.check_password((password_input)) == False and user_input != user_get:
                raise forms.ValidationError( "Passwords or username must be the same")
            return password_input
        # else:
        #     raise forms.ValidationError( "Account not registered!")
        
global new_user
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email', 'password' ]
    def clean(self):
        user_input     = self.cleaned_data['username']
        email_input    = self.cleaned_data['email']
        user_db  = User.objects.filter( username = user_input)
        email_db = User.objects.filter( email = email_input)
        password       = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        print(password, password_check, email_input)
        if password != password_check or (email_input is None):
            #raise ValidationError('Password do not match')
            self.add_error('password_check', '')
            self.add_error('__all__', 'Password do not match')
        if str(user_input) == str(*user_db) or str(email_input) == email_db:
            self.add_error('username', '')
            self.add_error('password', '')
            self.add_error('password_check', '')
            self.add_error('email', '')
            self.add_error('__all__', 'This username is already taken')
            # raise ValidationError('This account already used')
            

    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        new_user = User.objects.create_user(**self.cleaned_data)
        ProfileModel.objects.create(user = new_user, user_name=self.cleaned_data['username'], email=self.cleaned_data['email'])
        return new_user


class EditProfile(forms.ModelForm):
    nick = forms.CharField()
    class Meta:
        model  = ProfileModel
        fields = ['avatar', 'email', 'nick']
    def clean(self):
        nick_input  = self.cleaned_data['nick']
        email_input = self.cleaned_data['email']
        nick_db  = User.objects.filter( username = nick_input)
        email_db = User.objects.filter( email = email_input)

        if  str(*email_db) != "" or str(*nick_db) != "":
            self.add_error('email', '')
            self.add_error('nick', '')
            self.add_error('__all__', 'Email or nick already uses')
            #raise ValidationError('Email or nick already uses')
        
    def save(self, **kwargs):
        newUser    = User.objects.create(username = self.cleaned_data['nick'], email = self.cleaned_data['email'])
        newProfile = ProfileModel.objects.create(user=newUser, user_name=self.cleaned_data['nick'], email=self.cleaned_data['email'])
        return newProfile

class CreateQuestion(forms.ModelForm):

    title = forms.CharField()
    text  = forms.CharField(widget=forms.Textarea)
    tag   = forms.CharField()
    class Meta:
        model = QuestionModel
        fields = ['title', 'text']

    def clean(self):

        title_input = self.cleaned_data['title']
        text_input  = self.cleaned_data['text']

        title_db = QuestionModel.objects.filter( title = title_input)
        text_db  = QuestionModel.objects.filter( text = text_input)

        if  str(*title_db) != "" or str(*text_db) != "":
            self.add_error('title', '')
            self.add_error('text', '')
            self.add_error('__all__', 'This question is already exists')
            #raise ValidationError('This question is already uses')
        tag_input  = self.cleaned_data['tag']
        new_split = str(tag_input).split()      
        if len(new_split) > 3:
            self.add_error('tag', 'This tag only 3')
    global new_split  
    def save(self, kwargs):
        tag_input  = self.cleaned_data['tag']
        new_split = str(tag_input).split()
        initial = []
        for i in range(len(new_split)):
            new_tag  = TagModel.objects.create(id = 5*kwargs+i, title=new_split[i])
            initial.append(new_tag)

        #new_tag  = TagModel.objects.create(id = kwargs, title=self.cleaned_data['tag'] )
        users    = User.objects.all()
        # new_ask = QuestionModel.objects.create(user = users[randint(0,len(users))], title=self.cleaned_data['title'], text=self.cleaned_data['text'])
        new_ask   = QuestionModel.objects.create(id = kwargs, user = users[randint(0,len(users)-1)], title=self.cleaned_data['title'], text=self.cleaned_data['text'])
        new_ask.tags.set(*[initial])
        return new_ask


class CreateAnswer(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model  = AnswerModel
        fields = ['text']

    def save(self, question_id, user_id):
        new_ans   = AnswerModel.objects.create(user_id = user_id, question_id = question_id, text = self.cleaned_data['text'])
        
        return new_ans