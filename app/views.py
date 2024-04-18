from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.core.paginator import Paginator
from library.models import   User, QuestionManagerMy, AnswerModel, QuestionModel, TagModel, QuestionManager

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

def index(request):
    
    page = request.GET.get('page', 1)
    return render(request, template_name='index.html', context={'questions': paginate(questions, page)})

def question(request, question_id):

    #posts = Question.objects.all()
    page = request.GET.get('page', 1)
    return render(request, template_name='question.html', context={'questions': paginate(questions, page)})

def ask(request):
    
    return render(request, template_name='ask.html')

def base(request):
    
    return render(request, template_name='base.html')

def signup(request):
    
    return render(request, template_name='signup.html')

def login(request):
    us = User.objects.all()
    
    return render(request, template_name='login.html')

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
    popular_tag_list=QuestionManager.get_hot(self=QuestionModel.objects) [:5]

    questions_list= QuestionManager.get_new(self=QuestionModel.objects)
    tag_list      = TagModel.objects.all()[:3]
    return render(request, template_name='base.html', context={'questions': paginate(questions_list, page), 'questions_list' : questions_list, 'popular_tags': popular_tag_list, 'tag_list':tag_list})


# Список лучших вопросов
def best_questions(request):
    page = request.GET.get('page', 1)
    questions_list = QuestionManager.get_hot(self=QuestionModel.objects.all())
    tag_list      = TagModel.objects.all()[:3]
    popular_tag_list=QuestionManager.get_hot(self=QuestionModel.objects) [:5]
    return render(request, template_name='index.html', context={'questions': paginate(questions_list, page), 'tags' : tag_list, 'popular_tags': popular_tag_list})

# Список вопросов по тегу
def tag_questions(request, tag_id):
    page = request.GET.get('page', 1)
    question_list = QuestionManager.get_question_by_tag(cls=QuestionModel.objects, tag=str(int(tag_id)+1))
    tag_list      = QuestionManager.get_tag_questions  (cls=TagModel.objects,      tag=tag_id)
    popular_tag_list=QuestionManager.get_hot(self=QuestionModel.objects) [:5]
    return render(request, template_name='indextag.html', context={'questions': paginate(question_list, page), 'tags' : tag_list, 'popular_tags': popular_tag_list})

# Страница 1 вопроса со списоком ответов
def OneQuestion(request, question_id):
    answers_list=QuestionManager.get_one_questions(self=AnswerModel.objects)
    question_list = QuestionModel.objects.filter(id=question_id)
    page = request.GET.get('page', 1)
    popular_tag_list=QuestionManager.get_hot(self=QuestionModel.objects) [:5]
    tag_list      = QuestionManager.get_tag_questions(cls=TagModel.objects,      tag=str(int(question_id)-1))

    return render(request, template_name='question.html', context={'questions': paginate(answers_list, page), 'questions_list' : question_list, 'popular_tags': popular_tag_list, 'tags':tag_list})
