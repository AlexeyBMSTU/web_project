from itertools import count
from random import randint
from django.contrib import auth
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse
from pymysql import NULL
from library.models import   ProfileModel, User, AnswerModel, QuestionModel, TagModel, QuestionManager, TagManager, AnswerManager
from django.contrib.auth import login, authenticate
from .forms import CreateAnswer, CreateQuestion, LoginForm, RegisterForm, EditProfile
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.decorators.http import require_http_methods
# Create your views here.

def paginate(objects, page, per_page=5):
    paginator = Paginator(objects, per_page)
   
    return paginator.page(page)

#@login_required(login_url='login',redirect_field_name="continue")
#@login_required(login_url='login', redirect_field_name='next')

def ask( request ):

    popular_tag_list  = TagModel.objects.get_popular_tag()

    global questions_id

    if request.method == "GET" :
        ask_form = CreateQuestion()

    if request.method == "POST":
        ask_form = CreateQuestion(request.POST)

        if ask_form.is_valid():

            all_ask      = QuestionModel.objects.all()
            questions_id = len(all_ask)+1
            ask          = ask_form.save(questions_id)

            if ask is not None:
                all_ask      = QuestionModel.objects.all()
                questions_id = str(int(len(all_ask)))
                return redirect( reverse( 'question', args = [str( int( questions_id ) )] ) )
            
            else:
                return render( request, template_name='incorrect_login.html' )

    return render( request, template_name='ask.html', context={'form':ask_form, 'popular_tags': popular_tag_list} )



incorrect_count = 0
#@login_required
def signup( request ):

    global incorrect_count

    if request.method == "GET" :
        user_form = RegisterForm()

    if request.method == "POST":
        user_form = RegisterForm( request.POST )

        if user_form.is_valid():
            user = user_form.save()

            if user is not None:
                print("Registration succesfully")
                return redirect(reverse('login'))

        else:

            incorrect_count = incorrect_count + 1

            if incorrect_count > 2:
                incorrect_count = 0
                return render( request, template_name='incorrect_login.html' )
 
    return render( request, template_name='signup.html', context={'form':user_form} )

def log_out( request ):

    auth.logout( request )
    return redirect( reverse( 'login' ) )

#@login_required(login_url='login/', redirect_field_name='next')
#@require_http_methods(['GET', 'POST'])
def log_in( request ):

    global incorrect_count

    if request.method == "GET":
        login_form = LoginForm()
        
    if request.method == "POST":
        login_form = LoginForm( data = request.POST )

        if login_form.is_valid():
            username = login_form.cleaned_data.get( 'username' )
            password = login_form.cleaned_data.get( 'password' )
            user     = authenticate( request=request, username=username, password=password )

            if user is not None:
                login( request, user )
                print( "Successfully logged in" )
                return redirect( reverse( 'hot' ) )
            else:
                login_form.add_error( '__all__', 'This user is not registered' )
                login_form.add_error( 'username', '' )
                login_form.add_error( 'password', '' )
        else:
            incorrect_count = incorrect_count + 1

            if incorrect_count > 2:
                incorrect_count = 0
                return render( request, template_name='incorrect_login.html' )

    return render( request, template_name='login.html', context={'form': login_form} )

def edit_profile( request ):

    popular_tag_list  = TagManager.get_popular_tag()

    global incorrect_count

    if request.method == "GET" :
        profile_form = EditProfile()

    if request.method == "POST":
        profile_form = EditProfile( request.POST )

        if profile_form.is_valid():
            profile = profile_form.save()
            print( profile_form.cleaned_data )

            if profile is not None:

                print( "Edit succesfully" )
                return redirect( reverse( 'profile' ) )

    return render( request, template_name='profile_edit.html', context={'form':profile_form, 'popular_tags': popular_tag_list} )


def pageNotFound( request, exception ):
    return render( request, template_name='404.html', status=404 )
def handler500( request ):
    return render( request, template_name='500.html', status=500 )


def get_popular_tag():
    return TagModel.objects.get_popular_tag()

def get_page( request ):
    return request.GET.get( 'page', 1)
    

#Список новых вопросов
def new_questions( request ):
    
    page = get_page( request )

    questions_list = QuestionModel.objects.get_new_question_list()

    return render( request, template_name='base.html', context={'questions': paginate( questions_list, page ), 'questions_list' : questions_list, 'popular_tags': get_popular_tag()} )


# Список лучших вопросов
def best_questions( request ):

    
    page = get_page( request )

    questions_list = QuestionModel.objects.get_best_question_list()

    return render( request, template_name='index.html', context={'questions': paginate(questions_list, page), 'popular_tags': get_popular_tag()} )

# Список вопросов по тегу
def tag_questions( request, tag_id ):

    page = get_page( request )

    question_list = QuestionModel.objects.get_question_by_tag( tag_id )
    current_tag   = TagModel.objects.get_current_tag( tag_id )

    return render( request, template_name='indextag.html', context={'questions': paginate(question_list, page),  'popular_tags': get_popular_tag(), 'tag_list':current_tag} )

# Страница 1 вопроса со списоком ответов
def OneQuestion( request, question_id ):
   
    page = get_page( request )

    question_list = QuestionModel.objects.get_question_by_id( question_id )
    answers_list  = AnswerModel.objects.get_answer_with_id( question_id )


    if request.method == "GET" :
        answer_form = CreateAnswer()

    if request.method == "POST":
        answer_form = CreateAnswer( request.POST, question_id )

        if answer_form.is_valid():
            if request.user.id is None:
                return render( request, template_name='please_login_or_registr.html' )     
               
            ans = answer_form.save( question_id, request.user.id )
            
            if ans is not None:
                return redirect( reverse( 'question', args = [str( int( question_id ) )] ) )
            else:
                return render( request, template_name='incorrect_login.html' )

    return render( request, template_name='question.html', context={'answer_list': paginate( answers_list, page ), 'questions_list' : question_list, 'popular_tags': get_popular_tag(), 'form':answer_form } )
