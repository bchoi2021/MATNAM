from socket import fromshare
from tkinter import Widget
from tkinter.tix import Select
from django import forms
from .models import ShareBoard, ShareAnswer
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget
from django.forms.widgets import NumberInput


class BoardWriteForm(forms.ModelForm):
    title = forms.CharField(
        label='글 제목',
        widget=forms.TextInput(
            attrs={
                'placehoder' : '게시글 제목',
            }),
            required=True,
        )

    contents = SummernoteTextField()

    # options = (
    #     ('Python', '추천 부탁'),
    #     ('Javascript', '추천 급함')
    # )
    
    # board_name = forms.ChoiceField(
    #     label='게시판 선택',
    #     widget=forms.Select(),
    #     choices=options
    # )

    field_order = [
        'title',
        # 'board_name',
        'contents'
    ]

    class Meta:
        model = ShareBoard
        fields = [
            'title',
            'contents',
            # 'board_name'
        ]
        widgets = {
            'contents' : SummernoteWidget()
        } 

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title', '')
        contents = cleaned_data.get('contents', '')
        # board_name = cleaned_data.get('board_name', 'Python')

        if title == '':
            self.add_error('title', '글 제목을 입력하세요.')
        elif contents == '':
            self.add_error('contents', '글 내용을 입력하세요.')
        else:
            self.title = title
            self.contents = contents
            # self.board_name = board_name


class AnswerForm(forms.ModelForm):
    class Meta:
        model = ShareAnswer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }

