from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.core.paginator import Paginator
from django.utils.timezone import datetime
from django.db.models import Sum, Count, Avg, F, Q
from django.utils import timezone
from django.conf import settings
from skorunkac.polls.models import Session, Question, Answer, Poll, Category


def select_session(request):
    if request.method == 'POST':
        session = get_object_or_404(Session, id=request.POST.get('session'))
        return redirect(
            'init_poll', session.slug
        )

    return render(
        request,
        template_name='select_session.html',
        context={
            'sessions': Session.objects.filter(active=True)
        }
    )


class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['gender', 'age', 'education', 'lifestyle']


def init_poll(request, session_slug):
    session = get_object_or_404(Session, slug=session_slug, active=True)

    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.session = session
            poll.save()
            return redirect(
                'questions', poll.id, 1
            )

    return render(
        request,
        template_name='start.html',
        context={
            'session': session,
            'form': PollForm()
        }
    )


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']


def questions(request, poll_id, page_no):
    poll = get_object_or_404(Poll, id=poll_id)
    questions = Question.objects.filter(active=True)
    p = Paginator(questions, settings.QUESTIONS_PER_PAGE)
    page = p.page(page_no)

    if request.method == 'POST':
        for question in page.object_list:
            try:
                answer = int(request.POST.get(str(question.id)))
            except:
                pass
            else:
                if answer in range(0, 5):
                    Answer.objects.update_or_create(
                        poll=poll,
                        question=question,
                        defaults={
                            'answer': answer
                        }
                    )

        if page.has_next():
            return redirect(
                'questions', poll.id, page.next_page_number()
            )
        else:
            poll.ended = timezone.now()
            poll.score = round(
                100 * (poll.answer_set.aggregate(total_points=Sum('answer'))['total_points'] or 0) /
                Question.objects.filter(active=True).count() / MAX_POINTS_PER_QUESTION, 1
            )
            poll.save()
            return redirect(
                'result', poll.id
            )

    return render(
        request,
        template_name='questions.html',
        context={
            'paginator': p,
            'page': page,
            'page_no': page_no,
            'answer_form': AnswerForm(),
            'poll': poll,
        }
    )


MAX_POINTS_PER_QUESTION = 4


def result(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    scores_by_category = {}
    answers = poll.answer_set.all()
    for question in Question.objects.filter(active=True):
        category = question.category
        answer = answers.filter(question=question, poll=poll).first()
        points = answer and answer.answer or 0
        if category in scores_by_category:
            scores_by_category[category]['question_count'] += 1
            scores_by_category[category]['total_points'] += points
        else:
            scores_by_category[category] = {
                'question_count': 1,
                'total_points': points
            }
    for cat, val in scores_by_category.items():
        scores_by_category[cat]['score'] = round(
            100 / MAX_POINTS_PER_QUESTION * scores_by_category[cat]['total_points'] /
            scores_by_category[cat]['question_count'],
            1
        )
    scores_by_category = sorted(scores_by_category.items(), key=lambda x: x[1]['score'], reverse=True)
    session_score = Poll.objects.filter(session=poll.session).exclude(score__isnull=True).aggregate(
        avg=Avg('score'), count=Count('score')
    )
    session_score_today = Poll.objects.exclude(score__isnull=True).filter(
        session=poll.session, ended__date=datetime.today()
    ).aggregate(
        avg=Avg('score'), count=Count('score')
    )
    global_score = Poll.objects.exclude(score__isnull=True).aggregate(
        avg=Avg('score'), count=Count('score')
    )

    return render(
        request,
        template_name='result.html',
        context={
            'poll': poll,
            'score': poll.score,
            'scores_by_category': scores_by_category,
            'weakest_category': scores_by_category[len(scores_by_category)-1],
            'session_score': session_score,
            'session_score_today': session_score_today,
            'global_score': global_score,
        }
    )


def suggest(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    scores_by_category = {}
    answers = poll.answer_set.all()
    for question in Question.objects.filter(active=True):
        category = question.category
        answer = answers.filter(question=question, poll=poll).first()
        points = answer and answer.answer or 0
        if category in scores_by_category:
            scores_by_category[category]['question_count'] += 1
            scores_by_category[category]['total_points'] += points
        else:
            scores_by_category[category] = {
                'question_count': 1,
                'total_points': points
            }
    for cat, val in scores_by_category.items():
        scores_by_category[cat]['score'] = round(
            100 / MAX_POINTS_PER_QUESTION * scores_by_category[cat]['total_points'] /
            scores_by_category[cat]['question_count'],
            1
        )
    scores_by_category = sorted(scores_by_category.items(), key=lambda x: x[1]['score'], reverse=True)

    return render(
        request,
        template_name='suggestions.html',
        context={
            'poll': poll,
            'weakest_category': scores_by_category[len(scores_by_category)-1],
        }
    )
