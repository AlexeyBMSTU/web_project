from itertools import count
from random import randint
from django.contrib import auth
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse
from library.models import   ProfileModel, User, AnswerModel, QuestionModel, TagModel, QuestionManager, TagManager, AnswerManager
from django.contrib.auth import login, authenticate
from .forms import CreateAnswer, CreateQuestion, LoginForm, RegisterForm, EditProfile
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Count
# Create your views here.

questions = [
        {
               'id': i,
              'title': f'Question № {i}',
          'content': f'Long lorem ipsum {i}',
          'page_id': i+i+i+i
        }for i in range(1,30)
    ]

user = [{

    'id':i
} for i in range(1,10)
]
def paginate(objects, page, per_page=5):
    paginator = Paginator(objects, per_page)
   
    return paginator.page(page)

#@login_required(login_url='login',redirect_field_name="continue")
#@login_required(login_url='login', redirect_field_name='next')
def index(request):
    
    page = request.GET.get('page', 1)
    return render(request, template_name='index.html', context={'questions': paginate(questions, page)})

def question(request, question_id):

    #posts = Question.objects.all()
    page = request.GET.get('page', 1)
    return render(request, template_name='question.html', context={'questions': paginate(questions, page)})

def ask(request):

    popular_tag_list = QuestionManager.get_hot(self=QuestionModel.objects) [:2]

    global questions_id
    if request.method == "GET" :
        ask_form = CreateQuestion()
    if request.method == "POST":
        ask_form = CreateQuestion(request.POST)
        if ask_form.is_valid():
            all_ask = QuestionModel.objects.all()
            questions_id = len(all_ask)+1
            ask = ask_form.save(questions_id)

            if ask is not None:
                print("Question OK")
                all_ask = QuestionModel.objects.all()
                questions_id = str(int(len(all_ask)))
                return redirect(reverse('question', args = [str(int(questions_id))]))
        # else:
        #     ask_form.add_error('title', '')
        #     ask_form.add_error('text', '')
            #return render(request, template_name='incorrect_login.html')
    return render(request, template_name='ask.html', context={'form':ask_form, 'popular_tags': popular_tag_list})


def base(request):
    
    return render(request, template_name='base.html')

incorrect_count = 0

def signup(request):
    global incorrect_count
    if request.method == "GET" :
        user_form = RegisterForm()
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user is not None:
                print("Registration succesfully")
                return redirect(reverse('hot'))

        else:
            incorrect_count = incorrect_count + 1
            if incorrect_count > 2:
                incorrect_count = 0
                return render(request, template_name='incorrect_login.html')
 
    return render(request, template_name='signup.html', context={'form':user_form})

def log_out(request):
    auth.logout(request)
    return redirect(reverse('login'))

#@login_required(login_url='login/', redirect_field_name='next')


def log_in(request):
    global incorrect_count
    if request.method == "GET":
        login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("Successfully logged in")
                return redirect(request.GET.get('next', 'hot'))
            else:
                login_form.add_error('__all__', 'The user is not registered')
                login_form.add_error('username', '')
                login_form.add_error('password', '')
        else:
            incorrect_count = incorrect_count + 1
            if incorrect_count > 2:
                incorrect_count = 0
                return render(request, template_name='incorrect_login.html')

    return render(request, template_name='login.html', context={'form': login_form})

def edit_profile(request):
    popular_tag_list = QuestionManager.get_hot(self=QuestionModel.objects) [:2]

    global incorrect_count
    if request.method == "GET" :
        profile_form = EditProfile()
    if request.method == "POST":
        profile_form = EditProfile(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save()
            print(profile_form.cleaned_data)
            if profile is not None:
                print("Edit succesfully")
                return redirect(reverse('profile'))

    return render(request, template_name='profile_edit.html', context={'form':profile_form, 'popular_tags': popular_tag_list})

def profile(request):
    all_users = User.objects.all()
    nick = User.objects.filter(id = len(all_users)-1)
    email = User.objects.filter(id = len(all_users)-1)

    return render(request, template_name='profile.html', context={'nick': nick, 'email' : email})




def indextag(request):
    page = request.GET.get('page', 1)
    # return render(request, template_name='indextag.html', context={'question': paginate(questions, page=1), 'p1' : p1})
    return render(request, template_name='indextag.html', context={'questions': paginate(questions, page)})


def pageNotFound(request, exception):
    return render(request, template_name='404.html', status=404)
def handler500(request):
    return render(request, template_name='500.html', status=500)


## DATA BASE


#Список новых вопросов
def new_questions(request):
    
    page = request.GET.get('page', 1)

    popular_tag_list = TagManager.get_popular_tag(self = QuestionModel.objects )

    questions_list   = TagManager.get_new_question_list( self = QuestionModel.objects )

    return render(request, template_name='base.html', context={'questions': paginate(questions_list, page), 'questions_list' : questions_list, 'popular_tags': popular_tag_list})


# Список лучших вопросов
def best_questions(request):

    page = request.GET.get('page', 1)

    popular_tag_list = TagManager.get_popular_tag( self = QuestionModel.objects )

    questions_list   = TagManager.get_best_question_list( self = QuestionModel.objects )
    
    return render(request, template_name='index.html', context={'questions': paginate(questions_list, page), 'popular_tags': popular_tag_list})

# Список вопросов по тегу
def tag_questions(request, tag_id):

    page = request.GET.get('page', 1)

    popular_tag_list = TagManager.get_popular_tag( self = QuestionModel.objects )
    
    question_list    = QuestionManager.get_question_by_tag( self = QuestionModel.objects, tag_id = tag_id)

    return render(request, template_name='indextag.html', context={'questions': paginate(question_list, page),  'popular_tags': popular_tag_list, 'tag_id':tag_id})

# Страница 1 вопроса со списоком ответов
def OneQuestion(request, question_id):
    page = request.GET.get('page', 1)

    question_list    = QuestionManager.get_question_by_id( self = QuestionModel.objects, question_id = question_id)
    answers_list     = AnswerManager.get_answer_with_id(self = AnswerModel.objects, answer_id=question_list[0])

    popular_tag_list = QuestionManager.get_hot(self=QuestionModel.objects) [:2]

    author           = QuestionManager.get_author_with_id(self = User.objects, author_id = question_id)
    authors          = QuestionManager.get_all_users(self = User.objects)

    if str(*author) == "":
        author = User.objects.filter(id = str(int(len(authors))))
 
    if request.method == "GET" :
        answer_form = CreateAnswer()
    if request.method == "POST":
        answer_form = CreateAnswer(request.POST, question_id)
        if answer_form.is_valid():
            ans = answer_form.save(question_id, request.user.id)
            
            if ans is not None:
                return redirect(reverse('question', args = [str(int(question_id))]))
            
    return render(request, template_name='question.html', context={'answer_list': paginate(answers_list, page), 'questions_list' : question_list, 'popular_tags': popular_tag_list, 'form':answer_form, 'author':author})
