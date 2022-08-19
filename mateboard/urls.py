from django.urls import path
from mateboard.views import question_views, answer_views

app_name = 'mateboard'
urlpatterns = [
    path('index/',
         question_views.index, name='index'),
    path('', question_views.board_list, name='board_list'),
    path('write/', question_views.board_write, name='board_write'),
    path('detail/<int:pk>/', question_views.board_detail, name='board_detail'),
    path('detail/<int:pk>/delete/', question_views.board_delete, name='board_delete'),
    path('detail/<int:pk>/modify/', question_views.board_modify, name='board_modify'),
    path('<int:pk>/like/', question_views.like, name='like'),
    path('detail/<int:board_id>/answer_create/', answer_views.answer_create, name='answer_create'),

    path('detail/<int:board_id>/vote_question/', answer_views.vote_question, name='vote_question'),
    path('detail/<int:board_id>/vote_answer/', answer_views.vote_answer, name='vote_answer'),

    path('detail/<int:answer_id>/answer_delete/', answer_views.answer_delete, name='answer_delete'),
    path('detail/<int:answer_id>/answer_modify/', answer_views.answer_modify, name='answer_modify'),



]