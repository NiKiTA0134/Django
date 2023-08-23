from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .controlers import *
from .forms import *
from django.db.models import Count

from .models import Notification


def render_main_page(request):
    category_id = request.GET.get('id')
    if category_id:
        questions = get_all_questions_with_answers_for_category(category_id)
    else:
        questions = get_all_questions_with_answers()
    return render(request, 'main.html', context={'questions': questions})


def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            create_question_with_success_message(form, request)
        else:
            messages.error(request, 'There was an error while adding question, check your data and try again.')
        return redirect('/')


def create_answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)

        if form.is_valid():
            create_answer_with_success_message(form, request)
        else:
            messages.error(request, 'There was an error while adding answer, check your data and try again.')
        return redirect('/')


def question_page(request):
    question_id = request.GET.get('id')
    answer_form = AnswerForm()
    return render(request, 'question.html', {'question': get_question_by_id(question_id),
                                             'answers': get_answers_for_question(question_id).order_by('-up_votes'),
                                             'answer_form': answer_form})


def edit_question(request, question_id):
    return edit_record(request, Question, QuestionForm, question_id)


def edit_answer(request, answer_id):
    return edit_record(request, Answer, AnswerForm, answer_id)


def delete_object(request, object_id, object_name):
    match object_name:
        case 'question':
            return delete_record(request, Question, object_id)
        case 'Answer':
            return delete_record(request, Answer, object_id)


def delete_answer(request, answer_id):
    return delete_record(request, Answer, answer_id)


def delete_notification(request, notification_id):
    Notification.objects.filter(pk=notification_id).delete()

    return HttpResponse('')


def cancel_delete(request):
    return redirect('/my_questions')


def render_categories_page(request):
    categories = get_all_categories()
    return render(request, 'categories.html', {'categories': categories})


def user_questions(request):
    questions = get_all_questions_for_user(request.user)
    answers = get_all_answers_for_user(request.user)
    vote_count_question = Question.objects.filter(author=request.user).count()
    vote_count_answer = Answer.objects.filter(author=request.user).count()
    status = 'Beginner'
    next_status = 'Novice'
    questions_request = 1
    answers_requests = 1
    if vote_count_question == 0 and vote_count_answer == 0:
        status = 'Beginner'
        next_status = 'Novice'
        questions_request = 1
        answers_requests = 1
    if vote_count_question >= 1 and vote_count_answer >= 1:
        status = 'Novice'
        next_status = 'Intermediate'
        questions_request = 5
        answers_requests = 5
    if vote_count_question >= 5 and vote_count_answer >= 5:
        status = 'Intermediate'
        next_status = 'Experienced'
        questions_request = 10
        answers_requests = 10
    if vote_count_question >= 10 and vote_count_answer >= 10:
        status = 'Experienced'
        next_status = 'Expert'
        questions_request = 15
        answers_requests = 25
    if vote_count_question >= 15 and vote_count_answer >= 25:
        status = 'Expert'
        next_status = 'Intermediate'
        questions_request = 25
        answers_requests = 50
    if vote_count_question >= 25 and vote_count_answer >= 50:
        status = 'Master'
        next_status = 'Legend'
        questions_request = 50
        answers_requests = 100
    if vote_count_question >= 50 and vote_count_answer >= 100:
        status = 'Legend'
        next_status = '???'
        questions_request = '???'
        answers_requests = '???'
    notifications = get_all_notifications_for_user(request.user)
    print(notifications)
    return render(request, 'user.html', {'questions': questions, 'answers': answers, 'status': status, 'next_status': next_status, 'questions_request': questions_request, 'answers_requests': answers_requests,
                                        'notifications': notifications})


def search(request):
    search_query = request.GET.get('query')
    questions = qet_questions_by_search_query(search_query)
    return render(request, 'main.html', {'questions': questions})


def ask_question(request):
    question_form = QuestionForm()
    return render(request, 'ask_question.html', context={'question_form': question_form})


def vote(request, model, action, record_id):
    model_mapping = {
        'question': Question,
        'answer': Answer
    }
    model_class = model_mapping.get(model)

    record = get_object_or_404(model_class, pk=record_id)

    if isinstance(record, Answer):
        redirect_id = record.question.id
        print(record.question.id)
    else:
        redirect_id = record_id

    try:
        if action == 'upvote':
            record.upvote(request.user.id)
        elif action == 'downvote':
            record.downvote(request.user.id)
        if request.user != record.author:
            create_notification(request, record, action)
        resp_data = 'ok'
    except Exception as e:
        print(e)
        resp_data = str(e)

    return redirect(f'/question?id={redirect_id}')