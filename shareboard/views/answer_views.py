from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from user.models import User

from shareboard.forms import AnswerForm
from shareboard.models import ShareBoard, ShareAnswer



def answer_create(request, board_id):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    board = get_object_or_404(ShareBoard, id=board_id)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        writer = User.objects.get(user_id=login_session)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = writer  # 추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.question = board
            answer.save()
            return redirect(f'/shareboard/detail/{board_id}/')
    else:
        form = AnswerForm()
    context = {'question': board, 'form': form}
    return render(request, 'shareboard/board_detail.html', context)


def answer_delete(request, pk):
    login_session = request.session.get('login_session', '')
    board = get_object_or_404(ShareBoard, id=pk)

    if board.writer.user_id == login_session:
        board.delete()
        return redirect('/shareboard')
    else:
        return redirect(f'/shareboard/detail/{pk}/')



@login_required
def answer_modify(request, answer_id):
    login_session = request.session.get('login_session', '')
    

    answer = get_object_or_404(ShareAnswer, id=answer_id)

    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect(f'/shareboard/detail/{answer_id}/')

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        context = {'login_session': login_session,
    'form': form}
        if form.is_valid():
            answer.author = request.user
            answer.modify_at = timezone.now()
            answer.save()
            return redirect('shareboard:answer_modify')
    else:
        form = AnswerForm(instance=answer)
        return render(request, 'shareboard/answer_modify.html', context)



def vote_question(request, board_id):
    login_session = request.session.get('login_session', '')

    writer = User.objects.get(user_id=login_session)

    question = get_object_or_404(ShareBoard, pk=board_id)
    if request.user == writer:
        messages.error(request, '자신이 작성한 글에는 추천할 수 없습니다.')
    else:
        question.voter.add(writer)
    return redirect(f'/shareboard/detail/{board_id}/', {
        'question_id' : question.id,
        'login_session': login_session
        }
)



def vote_answer(request, board_id):
    login_session = request.session.get('login_session', '')

    author = User.objects.get(user_id=login_session)

    answer = get_object_or_404(ShareAnswer, id=board_id)
    if request.user == author:
        messages.error(request, '자신이 작성한 글에는 추천할 수 없습니다.')
    else:
        answer.voter.add(author)
    return redirect('/shareboard',  {
        'question_id':answer.question.id,
        'login_session': login_session
        }
        )


