from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email 

class UserCreateForm(FlaskForm):
    username = StringField('', validators=[DataRequired('사용자이름은 필수 입력항목입니다.'), Length(min=2,max=20)])
    password1 = PasswordField('', validators=[DataRequired('비밀번호는 필수 입력항목입니다.'),EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('',validators=[DataRequired('비밀번호 확인은 필수 입력항목입니다.')])
    email = EmailField('',validators=[DataRequired('이메일은 필수 입력항목입니다.'),Email(),Length(min=2,max=30)])
    private_key = StringField('',validators=[DataRequired('블로그코드는 필수 입력항목입니다.')])

class UserLoginForm(FlaskForm):
    email = StringField('이메일',validators=[DataRequired('이메일은 필수 입력항목입니다.'),Length(min=2,max=30)])
    password = PasswordField('비밀번호',validators=[DataRequired('비밀번호는 필수 입력항목입니다.')])

class DiaryForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목을 입력해주세요!'),Length(min=2,max=30)])
    content = StringField('내용', validators=[DataRequired('내용을 입력해주세요!')])
    private = SelectField('공개', choices=[('공개','공개'),('비공개','비공개')] )

class CommentForm(FlaskForm):
    content = StringField('내용', validators=[DataRequired('내용을 입력해주세요!')])

class Guest_bookForm(FlaskForm):
    content = StringField('내용', validators=[DataRequired('내용을 입력해주세요!')])

class BlogForm(FlaskForm):
    blog = StringField('블로그코드', validators=[DataRequired('이동하시려는 블로그코드를 입력해주세요!')])

class UserModifyForm(FlaskForm):
    password1 = PasswordField('비밀번호', validators=[EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호 확인')
    private_key = StringField('블로그코드',validators=[DataRequired()])
    introduction = TextAreaField('블로그 소개', validators=[DataRequired()])