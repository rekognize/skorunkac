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
        fields = ['gender', 'age', 'education', 'marital_status', 'hometown_size']


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
    p = Paginator(questions, settings.POLL_SETTINGS['QUESTIONS_PER_PAGE'])
    page = p.page(page_no)

    if request.method == 'POST':
        for question in page.object_list:
            try:
                answer = int(request.POST.get(str(question.id)))
            except:
                pass
            else:
                if answer in range(0, settings.POLL_SETTINGS['ANSWER_STEPS'] + 1):
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
            score = poll.answer_set.filter(
                question__inverse_score=False
            ).aggregate(total_points=Sum('answer'))['total_points'] or 0
            inverse_score = poll.answer_set.filter(
                question__inverse_score=True
            ).aggregate(total_points=Sum('answer'))['total_points'] or 0
            question_count = Question.objects.filter(active=True).count()
            inverse_question_count = Question.objects.filter(active=True).filter(inverse_score=True).count()
            poll.score = round(
                100 * (score + (settings.POLL_SETTINGS['ANSWER_STEPS'] * inverse_question_count - inverse_score)) /
                question_count / settings.POLL_SETTINGS['ANSWER_STEPS'], 1
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
            'poll_settings': settings.POLL_SETTINGS,
        }
    )


def result(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    scores_by_category = {}
    answers = poll.answer_set.all()
    for question in Question.objects.filter(active=True):
        category = question.category
        answer = answers.filter(question=question, poll=poll).first()
        points = 0
        if answer:
            points = answer.answer
            if answer.question.inverse_score:
                points = settings.POLL_SETTINGS['ANSWER_STEPS'] - answer.answer
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
            100 / settings.POLL_SETTINGS['ANSWER_STEPS'] * scores_by_category[cat]['total_points'] /
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
            'strongest_category': scores_by_category[0],
            'weakest_category': scores_by_category[len(scores_by_category)-1],
            'session_score': session_score,
            'session_score_today': session_score_today,
            'global_score': global_score,
            'poll_settings': settings.POLL_SETTINGS,
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
            100 / settings.POLL_SETTINGS['ANSWER_STEPS'] * scores_by_category[cat]['total_points'] /
            scores_by_category[cat]['question_count'],
            1
        )
    scores_by_category = sorted(scores_by_category.items(), key=lambda x: x[1]['score'], reverse=True)

    return render(
        request,
        template_name='suggestions.html',
        context={
            'poll': poll,
            'strongest_category': scores_by_category[0],
            'weakest_category': scores_by_category[len(scores_by_category)-1],
            'poll_settings': settings.POLL_SETTINGS,
        }
    )
