from re import T
from tabnanny import verbose
from tkinter import CASCADE
from django.db import models
from django.urls import reverse


class ShareBoard(models.Model):
    title = models.CharField(max_length=64, verbose_name='글 제목')
    contents = models.TextField(verbose_name='글 내용')
    writer = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='작성자')
    write_dttm = models.DateTimeField(auto_now_add=True, verbose_name='글 작성일')

    board_name = models.CharField(max_length=32, default='Python', verbose_name='게시판 종류')
    update_dttm = models.DateTimeField(auto_now_add=True, verbose_name='마지막 수정일')
    hits = models.PositiveBigIntegerField(default=0, verbose_name='조회수')

    like_users = models.ManyToManyField('user.User',
                            related_name='share_like_articles')
    voter = models.ManyToManyField('user.User', related_name='share_voter_question')


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'shareboard'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'


class ShareAnswer(models.Model):
    author = models.ForeignKey('user.User', on_delete=models.CASCADE,
                               related_name='share_author_answer', null=True, blank=True)
    question = models.ForeignKey(ShareBoard, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(null=True)
    voter = models.ManyToManyField('user.User', related_name='share_voter_answer')    


    def __str__(self):
        return self.content



