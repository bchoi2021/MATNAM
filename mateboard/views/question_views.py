from django.contrib import messages
from django.utils import timezone
from django.shortcuts import get_object_or_404
from urllib import response
from django.shortcuts import render, redirect, resolve_url
from mateboard.forms import MateBoardWriteForm, MateAnswerForm
from mateboard.models import MateBoard
from user.models import User
from user.decorators import login_required
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.db.models import Q, Count
import logging
logger = logging.getLogger('board')

def index(request):
    logger.info("INFO 레벨로 출력")

    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        question_list = MateBoard.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-write_dttm')
    elif so == 'popular':
        question_list = MateBoard.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-write_dttm')
    else:  # recent
        question_list = MateBoard.objects.order_by('-write_dttm')

    # 조회
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(author__username__icontains=kw) |  # 질문 작성자 검색
            Q(answer__author__username__icontains=kw)  # 답변 작성자 검색
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {
        'question_list': page_obj,
        'page': page, 
        'kw': kw, 
        'so': so,
    }
    return render(request, 'mateboard/board_list.html', context)

def board_list(request):    
    logger.info("INFO 레벨로 출력")
    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':

        question_list = MateBoard.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-write_dttm')

    elif so == 'popular':

        question_list = MateBoard.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-write_dttm')

    else:  # recent

        question_list = MateBoard.objects.order_by('-write_dttm')
    # 조회
    if kw:
        question_list = question_list.filter(
            Q(title__icontains=kw) |  # 제목 검색
            Q(contents__icontains=kw) |  # 내용 검색
            Q(writer__username__icontains=kw) |  # 질문 작성자 검색
            Q(answer__author__username__icontains=kw)  # 답변 작성자 검색
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    login_session = request.session.get('login_session', '')
    context = {
        'login_session': login_session,
        'question_list': page_obj,
        'page': page, 
        'kw': kw, 
        'so': so,
    }

    py_boards = MateBoard.objects.filter(
        board_name='Python').order_by('-write_dttm')
    # js_boards = Board.objects.filter(
    #     board_name='JavaScript').order_by('-write_dttm')

    # # page = int(request.GET.get('p', 1))
    # # paginator = Paginator(py_boards, 5)
    # # boards = paginator.get_page(page)

    context['py_boards'] = py_boards
    # context['js_boards'] = js_boards


    return render(request, 'mateboard/board_list.html', context)

    # return render(request, 'board/board_list.html', context)


@login_required
def board_write(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    if request.method == 'GET':
        write_form = MateBoardWriteForm()
        context['forms'] = write_form
        return render(request, 'mateboard/board_write.html', context)

    elif request.method == 'POST':
        write_form = MateBoardWriteForm(request.POST)

        if write_form.is_valid():
            writer = User.objects.get(user_id=login_session)
            board = MateBoard(
                title=write_form.title,
                contents=write_form.contents,
                writer=writer,
            )
            board.save()


            return redirect('/mateboard')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'mateboard/board_write.html', context)


def board_detail(request, pk):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    board = get_object_or_404(MateBoard, id=pk)
    context['board'] = board

    # 글쓴이인지 확인
    if board.writer.user_id == login_session:
        context['writer'] = True
    else:
        context['writer'] = False

    comment_form = MateAnswerForm()

    # response = render(request, 'board/board_detail.html', context)
    response = render(request, 'mateboard/board_detail.html', {
        'board': board,
        'comment_form': comment_form,
        'login_session': login_session,
    }
    )

    # 조회수 기능 (쿠키 이용)
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(
        hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get('hitboard', '_')

    if f'_{pk}_' not in cookie_value:
        cookie_value += f'{pk}_'
        response.set_cookie('hitboard', value=cookie_value,
                            max_age=max_age, httponly=True)
        board.hits += 1
        board.save()
    return response


def board_delete(request, pk):
    login_session = request.session.get('login_session', '')
    board = get_object_or_404(MateBoard, id=pk)

    if board.writer.user_id == login_session:
        board.delete()
        return redirect('/board')
    else:
        return redirect(f'/board/detail/{pk}/')


@login_required
def board_modify(request, pk):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    board = get_object_or_404(MateBoard, id=pk)
    context['board'] = board

    if board.writer.user_id != login_session:
        return redirect(f'/board/detail/{pk}/')

    if request.method == 'GET':
        write_form = MateBoardWriteForm(instance=board)
        context['forms'] = write_form
        return render(request, 'board/board_modify.html', context)

    elif request.method == 'POST':
        write_form = MateBoardWriteForm(request.POST)

        if write_form.is_valid():
            board.title = write_form.title,
            board.contents = write_form.contents,
            board.board_name = write_form.board_name

            board.save()
            return redirect('/board')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board/board_modify.html', context)





def like(request, pk):
    article = get_object_or_404(MateBoard, pk=pk)

    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)
        return redirect('board:board_detail', article.pk)




