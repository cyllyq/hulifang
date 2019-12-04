import datetime
import random


from examination.models import ExamQuestion, SectionQuestion, DayQuestion, Question
from operation.models import QuestionFav, WrongQuestion
from django.db.models import F, IntegerField, Value


def get_questions(related, question_type=None, with_answer=True, with_analysis=True, start=0, end=20, fav=True, user=None):
    kwargs = {
        'record_id': F('id'),
        'q_id': F('question__id'),
        'stem': F('question__stem'),
        'title': F('question__title'),
        'choice_a': F('question__choice_a'),
        'choice_b': F('question__choice_b'),
        'choice_c': F('question__choice_c'),
        'choice_e': F('question__choice_e'),
        'choice_d': F('question__choice_d'),
        'image': F('question__image'),
        'video': F('question__video'),
    }
    if with_answer:
        kwargs['answer'] = F('question__answer')
    if with_analysis:
        kwargs['analysis'] = F('question__analysis')
    if question_type == 'exam':
        question_records = ExamQuestion.objects.select_related('question').filter(
        examination__id=related).values('number', **kwargs).annotate(is_fav=Value(0, IntegerField()))
    elif question_type == 'section':
        question_records = SectionQuestion.objects.select_related('question').filter(
        section__id=related).values('number', **kwargs).annotate(is_fav=Value(0, IntegerField()))
    elif question_type == 'day':
        question_records = DayQuestion.objects.select_related('question').filter(
        day_attendance__create_time=related).values('number', **kwargs).annotate(is_fav=Value(0, IntegerField()))
    elif question_type == 'wrong':
        question_records = WrongQuestion.objects.select_related('question').filter(
            user=related,).values('wrong_count', **kwargs).annotate(is_fav=Value(0, IntegerField()))
    else:
        return Question.objects.all()[start:end].values().annotate(is_fav=Value(0, IntegerField()))

    #添加收藏字段
    if user:
        fav_ids = get_fav_questions(user=user)
        for question_record in question_records:
            if question_record['q_id'] in fav_ids:
                question_record['is_fav'] = 1
    return question_records
    '''
    for question_record in question_records:
        question = {}
        question['id'] = question_record.question.id
        question['number'] = question_record.number
        question['stem'] = question_record.question.stem
        question['title'] = question_record.question.title
        question['choice_a'] = question_record.question.choice_a
        question['choice_b'] = question_record.question.choice_b
        question['choice_c'] = question_record.question.choice_c
        question['choice_d'] = question_record.question.choice_d
        question['choice_e'] = question_record.question.choice_e
        question['image'] = question_record.question.image
        question['video'] = question_record.question.video
        question['is_fav'] = 1 if question['id'] in fav_ids else 0
        if with_answer:
            question['answer'] = question_record.question.answer
        if with_analysis:
            question['analysis'] = question_record.question.analysis
        questions.append(question)
    return questions
    '''


def correct_question_count(questions, related=None, question_type=None):
    '''
    params:
    {'id': 'answer', 'id': 'answer'...}

    return: (total, right_count)
    '''
    question_ids = questions.keys()
    if question_type == 'exam':
        right_answers = dict(ExamQuestion.objects.filter(id__in=question_ids, examination__id=related).values_list('question__id', 'question__answer'))
    elif question_type == 'day':
        right_answers = dict(DayQuestion.objects.filter(id__in=question_ids, day_attendance__create_time=related).values_list('question__id', 'question__answer'))
    else:
        right_answers = dict(Question.objects.values_list('id', 'answer').filter(id__in=question_ids).values_list('id', 'answer'))
    right_count = 0
    right_ids = right_answers.keys()
    for key, value in questions.items():
        key = int(key)
        if key in right_ids and right_answers[key] == value:
            right_count += 1
    return len(right_answers), right_count


def get_code(length=6):
    return str(random.randint(100000, 999999))


def get_fav_questions(user):
    return QuestionFav.objects.filter(user=user).values_list('question__id')
