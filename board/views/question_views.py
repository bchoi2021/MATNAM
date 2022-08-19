from django.contrib import messages
from django.utils import timezone
from django.shortcuts import get_object_or_404
from urllib import response
from django.shortcuts import render, redirect, resolve_url
from board.forms import BoardWriteForm, AnswerForm, FreeBoardWriteForm, FreeAnswerForm, PostSearchForm
from board.models import Board, FreeBoard
from user.models import User
from user.decorators import login_required
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.db.models import Q, Count
import logging
from django.views.generic import FormView


from django import forms

logger = logging.getLogger('board')

def index(request):
    logger.info("INFO 레벨로 출력")

    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        question_list = Board.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-write_dttm')
    elif so == 'popular':
        question_list = Board.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-write_dttm')
    else:  # recent
        question_list = Board.objects.order_by('-write_dttm')

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
    return render(request, 'board/board_list.html', context)

def board_list(request):    
    logger.info("INFO 레벨로 출력")
    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':

        question_list = Board.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-write_dttm')

    elif so == 'popular':

        question_list = Board.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-write_dttm')

    else:  # recent

        question_list = Board.objects.order_by('-write_dttm')
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

    py_boards = Board.objects.filter(
        board_name='Python').order_by('-write_dttm')
    # js_boards = Board.objects.filter(
    #     board_name='JavaScript').order_by('-write_dttm')

    # # page = int(request.GET.get('p', 1))
    # # paginator = Paginator(py_boards, 5)
    # # boards = paginator.get_page(page)

    context['py_boards'] = py_boards
    # context['js_boards'] = js_boards


    return render(request, 'board/board_list.html', context)

    # return render(request, 'board/board_list.html', context)


@login_required
def board_write(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    if request.method == 'GET':
        write_form = BoardWriteForm()
        context['forms'] = write_form
        return render(request, 'board/board_write.html', context)

    elif request.method == 'POST':
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            writer = User.objects.get(user_id=login_session)
            board = Board(
                title=write_form.title,
                contents=write_form.contents,
                writer=writer,
            )
            board.save()


            return redirect('/board')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board/board_write.html', context)


def board_detail(request, pk):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    board = get_object_or_404(Board, id=pk)
    context['board'] = board

    # 글쓴이인지 확인
    if board.writer.user_id == login_session:
        context['writer'] = True
    else:
        context['writer'] = False

    comment_form = AnswerForm()

    # response = render(request, 'board/board_detail.html', context)
    response = render(request, 'board/board_detail.html', {
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
    board = get_object_or_404(Board, id=pk)

    if board.writer.user_id == login_session:
        board.delete()
        return redirect('/board')
    else:
        return redirect(f'/board/detail/{pk}/')


@login_required
def board_modify(request, pk):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    board = get_object_or_404(Board, id=pk)
    context['board'] = board

    if board.writer.user_id != login_session:
        return redirect(f'/board/detail/{pk}/')

    if request.method == 'GET':
        write_form = BoardWriteForm(instance=board)
        context['forms'] = write_form
        return render(request, 'board/board_modify.html', context)

    elif request.method == 'POST':
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            board.title = write_form.title,
            board.contents = write_form.contents,


            board.save()
            return redirect('/board')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board/board_modify.html', context)





def like(request, pk):
    article = get_object_or_404(Board, pk=pk)

    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)
        return redirect('board:board_detail', article.pk)


# Free

def free_board_list(request):    
    logger.info("INFO 레벨로 출력")
    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        question_list = FreeBoard.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-write_dttm')
    elif so == 'popular':
        question_list = FreeBoard.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-write_dttm')
    else:  # recent
        question_list = FreeBoard.objects.order_by('-write_dttm')

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
        'so': so
    }

    py_boards = FreeBoard.objects.filter(
        board_name='Python').order_by('-write_dttm')
    # js_boards = Board.objects.filter(
    #     board_name='JavaScript').order_by('-write_dttm')

    # # page = int(request.GET.get('p', 1))
    # # paginator = Paginator(py_boards, 5)
    # # boards = paginator.get_page(page)

    context['py_boards'] = py_boards
    # context['js_boards'] = js_boards


    return render(request, 'board/free_board_list.html', context)

    # return render(request, 'board/board_list.html', context)


@login_required
def free_board_write(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    if request.method == 'GET':
        write_form = FreeBoardWriteForm()
        context['forms'] = write_form
        return render(request, 'board/free_board_write.html', context)

    elif request.method == 'POST':
        write_form = FreeBoardWriteForm(request.POST)

        if write_form.is_valid():
            writer = User.objects.get(user_id=login_session)
            board = FreeBoard(
                title=write_form.title,
                contents=write_form.contents,
                writer=writer,
                board_name=write_form.board_name
            )
            board.save()
            return redirect('/board/free_board')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board/free_board_write.html', context)


def free_board_detail(request, pk):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    board = get_object_or_404(FreeBoard, id=pk)
    context['board'] = board

    # 글쓴이인지 확인
    if board.writer.user_id == login_session:
        context['writer'] = True
    else:
        context['writer'] = False

    comment_form = FreeAnswerForm()

    # response = render(request, 'board/board_detail.html', context)
    response = render(request, 'board/free_board_detail.html', {
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


def free_board_delete(request, pk):
    login_session = request.session.get('login_session', '')
    board = get_object_or_404(FreeBoard, id=pk)

    if board.writer.user_id == login_session:
        board.delete()
        return redirect('/board/free_board')
    else:
        return redirect(f'/board/detail/{pk}/free/')


@login_required
def free_board_modify(request, pk):
    login_session = request.session.get('login_session', '')
    context = {'login_session': login_session}

    board = get_object_or_404(FreeBoard, id=pk)
    context['board'] = board

    if board.writer.user_id != login_session:
        return redirect(f'/board/detail/{pk}/free/')

    if request.method == 'GET':
        write_form = FreeBoardWriteForm(instance=board)
        context['forms'] = write_form
        return render(request, 'board/free_board_modify.html', context)

    elif request.method == 'POST':
        write_form = FreeBoardWriteForm(request.POST)

        if write_form.is_valid():
            board.title = write_form.title,
            board.contents = write_form.contents,
            board.board_name = write_form.board_name

            board.save()
            return redirect('/board/free_board')
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board/free_board_modify.html', context)



def search(request):
  content_list = Board.objects.all()
  search = request.GET.get('search','')
  if search:
    search_list = content_list.filter(
      Q(title__icontains = search) | #제목
      Q(contents = search) 
    )
  paginator = Paginator(search_list,5)
  page = request.GET.get('page','')
  posts = paginator.get_page(page)
  board = Board.objects.all()

  return render(request, 'board/board_list.html',{'posts':posts, 'Board':board, 'search':search})


# # 검색 기능
def search(request):
    board = Board.objects.all().order_by('-id')

    q = request.POST.get('q', "") 

    if q:
        board = board.filter(title__icontains=q)
        return render(request, 'board/search.html', {'board' : board, 'q' : q})
    
    else:
        return render(request, 'board/search.html')

# class SearchFormView(FormView):
#     form_class = PostSearchForm
#     template_name = 'board/post_search.html'

#     def form_valid(self, form):
#         searchWord = form.cleaned_data['search_word']
#         post_list = Board.objects.filter(Q(title__icontains=searchWord) | Q(description__icontains=searchWord) | Q(content__icontains=searchWord)).distinct()

#         context = {}
#         context['form'] = form
#         context['search_term'] = searchWord
#         context['object_list'] = post_list

#         return render(self.request, self.template_name, context)