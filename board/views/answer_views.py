from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from user.models import User

from board.forms import AnswerForm, FreeAnswerForm
from board.models import Board, Answer, FreeBoard, FreeAnswer


@login_required
def answer_create(request, board_id):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    board = get_object_or_404(Board, id=board_id)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        writer = User.objects.get(user_id=login_session)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = writer  # 추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.question = board
            answer.save()
            return redirect(f'/board/detail/{board_id}/')
    else:
        form = AnswerForm()
    context = {'question': board, 'form': form}
    return render(request, 'board/board_detail.html', context)


def answer_delete(request, pk):
    login_session = request.session.get('login_session', '')
    board = get_object_or_404(Board, id=pk)

    if board.writer.user_id == login_session:
        board.delete()
        return redirect('/board')
    else:
        return redirect(f'/board/detail/{pk}/')



@login_required
def answer_modify(request, answer_id):
    login_session = request.session.get('login_session', '')
    

    answer = get_object_or_404(Answer, id=answer_id)

    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect(f'/board/detail/{answer_id}/')

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        context = {'login_session': login_session,
    'form': form}
        if form.is_valid():
            answer.author = request.user
            answer.modify_at = timezone.now()
            answer.save()
            return redirect('board:answer_modify')
    else:
        form = AnswerForm(instance=answer)
        return render(request, 'board/answer_modify.html', context)


@login_required
def vote_question(request, board_id):
    login_session = request.session.get('login_session', '')

    writer = User.objects.get(user_id=login_session)

    question = get_object_or_404(Board, pk=board_id)
    if request.user == writer:
        messages.error(request, '자신이 작성한 글에는 추천할 수 없습니다.')
    else:
        question.voter.add(writer)
    return redirect(f'/board/detail/{board_id}/', {
        'question_id' : question.id,
        'login_session': login_session
        }
)


@login_required
def vote_answer(request, board_id):
    login_session = request.session.get('login_session', '')

    author = User.objects.get(user_id=login_session)

    answer = get_object_or_404(Answer, id=board_id)
    if request.user == author:
        messages.error(request, '자신이 작성한 글에는 추천할 수 없습니다.')
    else:
        answer.voter.add(author)
    return redirect('/board',  {
        'question_id':answer.question.id,
        'login_session': login_session
        }
        )





#Free
@login_required
def free_answer_create(request, board_id):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    board = get_object_or_404(Board, id=board_id)

    if request.method == "POST":
        form = FreeAnswerForm(request.POST)
        writer = User.objects.get(user_id=login_session)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = writer  # 추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.question = board
            answer.save()
            return redirect(f'/board/detail/{board_id}/free/')
    else:
        form = FreeAnswerForm()
    context = {'question': board, 'form': form}
    return render(request, 'board/free_board_detail.html', context)


def free_answer_delete(request, pk):
    login_session = request.session.get('login_session', '')
    board = get_object_or_404(FreeBoard, id=pk)

    if board.writer.user_id == login_session:
        board.delete()
        return redirect('/board/free_board')
    else:
        return redirect(f'/board/detail/{pk}/free/')



@login_required
def free_answer_modify(request, answer_id):
    login_session = request.session.get('login_session', '')
    

    answer = get_object_or_404(FreeAnswer, id=answer_id)

    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect(f'/board/detail/{answer_id}/free/')

    if request.method == 'POST':
        form = FreeAnswerForm(request.POST, instance=answer)
        context = {'login_session': login_session,
    'form': form}
        if form.is_valid():
            answer.author = request.user
            answer.modify_at = timezone.now()
            answer.save()
            return redirect('board:free_answer_modify')
    else:
        form = FreeAnswerForm(instance=answer)
        return render(request, 'board/free_answer_modify.html', context)


@login_required
def free_vote_question(request, board_id):
    login_session = request.session.get('login_session', '')

    writer = User.objects.get(user_id=login_session)

    question = get_object_or_404(FreeBoard, pk=board_id)
    if request.user == writer:
        messages.error(request, '자신이 작성한 글에는 추천할 수 없습니다.')
    else:
        question.voter.add(writer)
    return redirect(f'/board/detail/{board_id}/free/', {
        'question_id' : question.id,
        'login_session': login_session
        }
)


@login_required
def free_vote_answer(request, board_id):
    login_session = request.session.get('login_session', '')

    author = User.objects.get(user_id=login_session)

    answer = get_object_or_404(FreeAnswer, id=board_id)
    if request.user == author:
        messages.error(request, '자신이 작성한 글에는 추천할 수 없습니다.')
    else:
        answer.voter.add(author)
    return redirect('/free_board',  {
        'question_id':answer.question.id,
        'login_session': login_session
        }
        )
