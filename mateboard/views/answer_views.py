from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from user.models import User

from mateboard.forms import MateAnswerForm
from mateboard.models import MateBoard, MateAnswer


@login_required
def answer_create(request, board_id):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    board = get_object_or_404(MateBoard, id=board_id)

    if request.method == "POST":
        form = MateAnswerForm(request.POST)
        writer = User.objects.get(user_id=login_session)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = writer  # 추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.question = board
            answer.save()
            return redirect(f'/mateboard/detail/{board_id}/')
    else:
        form = MateAnswerForm()
    context = {'question': board, 'form': form}
    return render(request, 'mateboard/board_detail.html', context)


def answer_delete(request, pk):
    login_session = request.session.get('login_session', '')
    board = get_object_or_404(MateBoard, id=pk)

    if board.writer.user_id == login_session:
        board.delete()
        return redirect('/mateboard')
    else:
        return redirect(f'/mateboard/detail/{pk}/')



@login_required
def answer_modify(request, answer_id):
    login_session = request.session.get('login_session', '')
    

    answer = get_object_or_404(MateAnswer, id=answer_id)

    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect(f'/mateboard/detail/{answer_id}/')

    if request.method == 'POST':
        form = MateAnswerForm(request.POST, instance=answer)
        context = {'login_session': login_session,
    'form': form}
        if form.is_valid():
            answer.author = request.user
            answer.modify_at = timezone.now()
            answer.save()
            return redirect('mateboard:answer_modify')
    else:
        form = MateAnswerForm(instance=answer)
        return render(request, 'mateboard/answer_modify.html', context)


@login_required
def vote_question(request, board_id):
    login_session = request.session.get('login_session', '')

    writer = User.objects.get(user_id=login_session)

    question = get_object_or_404(MateBoard, pk=board_id)
    if request.user == writer:
        messages.error(request, '자신이 작성한 글에는 추천할 수 없습니다.')
    else:
        question.voter.add(writer)
    return redirect(f'/mateboard/detail/{board_id}/', {
        'question_id' : question.id,
        'login_session': login_session
        }
)


@login_required
def vote_answer(request, board_id):
    login_session = request.session.get('login_session', '')

    author = User.objects.get(user_id=login_session)

    answer = get_object_or_404(MateAnswer, id=board_id)
    if request.user == author:
        messages.error(request, '자신이 작성한 글에는 추천할 수 없습니다.')
    else:
        answer.voter.add(author)
    return redirect('/mateboard',  {
        'question_id':answer.question.id,
        'login_session': login_session
        }
        )