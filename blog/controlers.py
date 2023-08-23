from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from .models import Question, Answer, Category, Notification


def get_all_questions():
    return Question.objects.all().order_by('-up_votes')


def get_question_by_id(question_id):
    return Question.objects.get(pk=question_id)


def get_answers_for_question(question_id):
    return Answer.objects.all().filter(question=question_id)


def get_all_answers():
    return Answer.objects.all()


def get_all_questions_with_answers_for_category(category_id):
    return get_all_questions().filter(category=int(category_id)).prefetch_related('answer_set')


def get_all_categories():
    return Category.objects.all()


def get_all_questions_with_answers():
    return get_all_questions().prefetch_related('answer_set')


def create_question_with_success_message(form, request):
    question = form.save(commit=False)
    question.author = request.user
    question.publish()
    messages.success(request, message='Question asked!')


def edit_record(request, model_class, form_class, record_id):
    record = get_object_or_404(model_class, pk=record_id)
    if request.method == 'POST':
        form = form_class(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = form_class(instance=record)
    return render(request, 'edit_record.html', {'form': form, 'model': record.__class__.__name__})


def delete_record(request, model_class, record_id):
    record = get_object_or_404(model_class, pk=record_id)
    if request.method == 'POST':
        record.delete()
        return redirect('/my_questions')
    else:
        return render(request, 'delete_record.html', {'record': record, 'model': record.__class__.__name__})


def create_answer_with_success_message(form, request):
    answer = form.save(commit=False)
    answer.author = request.user
    question_pk = request.POST.get('pk')
    question = Question.objects.get(pk=question_pk)
    answer.question = question
    answer.publish()
    messages.success(request, message='Answer published!')


def get_all_questions_for_user(user):
    return Question.objects.all().filter(author=user)


def get_all_answers_for_user(user):
    return Answer.objects.all().filter(author=user)


def get_all_notifications_for_user(user):
    return Notification.objects.all().filter(Q(to_user=user) and ~Q(from_user=user))


def qet_questions_by_search_query(query):
    return Question.objects.filter(Q(title__icontains=query) or Q(text__icontains=query))


def get_user_by_id(user_id):
    return User.objects.get(pk=user_id)


def create_notification(request, record, action):
    n = Notification()

    n.from_user = get_user_by_id(request.user.id)
    n.to_user = record.author
    n.post_id = record.id
    n.post_type = type(record).__name__
    n.action = action
    n.save()