from django import forms
from .models import User
from argon2 import PasswordHasher, exceptions

class RegisterForm(forms.ModelForm):
    user_id = forms.CharField(
        label='아이디',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class' : 'text_area1',
                'placeholder' : '아이디'
                # 'placeholder':"아이디",
                # 'type':"text",
                # 'id':"username",
                # 'name':"username",
                # 'class':"text_area1",
            }
        ),
        error_messages={
            'required' : '아이디를 입력해주세요.',
            'unique' : '중복된 아이디입니다.'}
    )

    user_pw = forms.CharField(
        label='비밀번호',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'text_area',
                'placeholder' : '비밀번호'
                # 'placeholder':"비밀번호",
                # 'type':"text",
                # 'id':"username",
                # 'name':"username",
                # 'class':"text_area",
            }
        ),
        error_messages={'required' : '비밀번호를 입력해주세요.'}
    )

    user_pw_confirm = forms.CharField(
        label='비밀번호 확인',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'text_area',
                'placeholder' : '비밀번호 확인'
                # 'placeholder':"비밀번호 확인",
                # 'type':"text",
                # 'id':"username",
                # 'name':"username",
                # 'class':"text_area",
            }
        ),
        error_messages={'required' : '비밀번호가 일치하지 않습니다.'}
    )

    user_name = forms.CharField(
        label='닉네임',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class' : 'text_area2',
                'placeholder' : '이름'
                # 'placeholder':"닉네임",
                # 'type':"text",
                # 'id':"username",
                # 'name':"username",
                # 'class':"text_area2",
            }
        ),
        error_messages={'required' : '닉네임을 입력해주세요.'}
    )   

    user_email = forms.EmailField(
        label='이메일',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class' : 'text_area2',
                'placeholder' : '이메일'
                # 'placeholder':"이메일",
                # 'type':"text",
                # 'id':"username",
                # 'name':"username",
                # 'class':"text_area2",
            }
        ),
        error_messages={'required' : '이메일을 입력해주세요.'}
    )   

    field_order = [
        'user_id',
        'user_pw', 
        'user_pw_confirm',
        'user_name',
        'user_email',
    ]

    class Meta:
        model = User
        fields = [
            'user_id',
            'user_pw', 
            'user_name',
            'user_email',
        ]

    def clean(self):
        cleaned_data = super().clean()

        user_id = cleaned_data.get('user_id','')
        user_pw = cleaned_data.get('user_pw','')
        user_pw_confirm = cleaned_data.get('user_pw_confirm','')
        user_name = cleaned_data.get('user_name','')
        user_email = cleaned_data.get('user_email','')

        if user_pw != user_pw_confirm:
            return self.add_error('user_pw_confirm', '비밀번호가 다릅니다.')
        elif not (4 <= len(user_id) <= 16):
            return self.add_error('user_id', '아이디는 4~16자로 입력해 주세요.')
        elif 8 > len(user_pw) :
            return self.add_error('user_pw', '비밀번호는 8자 이상으로 적어주세요.')
        else:
            self.user_id = user_id
            self.user_pw = PasswordHasher().hash(user_pw)
            self.user_pw_confirm = user_pw_confirm
            self.user_name = user_name
            self.user_email = user_email

class LoginForm(forms.Form):
    user_id = forms.CharField(
        max_length=32,
        label='아이디',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class' : 'text_input',
                'placeholder' : '아이디'
                # 'placeholder':"아이디를 입력하세요.",
                # 'type':"text",
                # 'id':"username",
                # 'name':"username",
                # 'class':"user-id",
            }
        ),
        error_messages={
            'required' : '아이디를 입력해주세요.'}
    )




    user_pw = forms.CharField(
        max_length=128,
        label='비밀번호',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'text_input',
                'placeholder' : '비밀번호'
                # 'placeholder':"비밀번호를 입력하세요.",
                # 'type':"text",
                # 'id':"password",
                # 'name':"password",
                # 'class':"user-pw",
            }
        ),
        error_messages={
            'required' : '비밀번호를 입력해주세요.'}
    )

    field_order = [
        'user_id',
        'user_pw',
    ]

    def clean(self):
        cleaned_data = super().clean() 

        user_id = cleaned_data.get('user_id','')
        user_pw = cleaned_data.get('user_pw','')

        if user_id == '':
            return self.add_error('user_id', '아이디를 다시 입력해 주세요.')
        elif user_pw == '':
            return self.add_error('user_pw', '비밀번호를 다시 입력해 주세요.')
        else:
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return self.add_error('user_id', '아이디가 존재하지 않습니다.')
            
            try:
                PasswordHasher().verify(user.user_pw, user_pw)
            except exceptions.VerifyMismatchError:
                return self.add_error('user_pw', '비밀번호가 다릅니다.')
            
            self.login_session = user.user_id