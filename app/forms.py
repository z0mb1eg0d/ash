from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField, DecimalField
from wtforms.validators import DataRequired, Email, Optional

class LoginForm(FlaskForm):
    username = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')

class RegisterForm(FlaskForm):
   username = StringField('Имя пользователя', validators=[DataRequired()])
   email = StringField('Почта', validators=[Email()])
   role = StringField('Кто ты по жизни', validators=[DataRequired()])
   password1 = PasswordField('Пароль', validators=[DataRequired()])
   password2 = PasswordField('Повторите Пароль', validators=[DataRequired()])
   submit = SubmitField('Регистрация')
   position = StringField('Должность', validators=[])
   department_number = DecimalField('№ Кафедры', validators=[Optional()])
   rank = StringField('Звание', validators=[])
   record_num = IntegerField('№ Зачетки', validators=[Optional()])
   group_num =IntegerField('№ Группы', validators=[Optional()])

class AddWorkForm(FlaskForm):
  title = StringField('Название работы', validators=[DataRequired()])
  theme = StringField('Тема', validators=[DataRequired()])
  conference = StringField('Название конференции', validators=[DataRequired()])
  conference_number = StringField('Номер конференции', validators=[DataRequired()])
  submit = SubmitField('Добавить научную работу')

class AddConferenceForm(FlaskForm):
  title = StringField('Название Конференции', validators=[DataRequired()]) 
  number = IntegerField('Номер Конференции', validators=[DataRequired()])
  theme = StringField('Тема Конференции', validators=[DataRequired()])
  date = DateField('Дата Проведения (Г.М.Д)', format='%Y.%m.%d' , validators=[DataRequired()])
  submit = SubmitField('Добавить Конференцию')

class Works(FlaskForm):
  submit = SubmitField('Пук Пук')
  names = StringField()

class IndexForm(FlaskForm):
  group = IntegerField('Номер группы')
  submit = SubmitField('Добавить группу')
  grant = StringField('Степуха')
  s_num = IntegerField('Зачетка')
  submit_s = SubmitField('Пык-Пык')
  st_del_id = StringField('Кого убиваем')
  submit_st_del = SubmitField('Чик')
  gr_del_num = IntegerField()
  gr_del = SubmitField('Чик группу')
  prep_del = StringField()
  prep_del_s = SubmitField('Чик препода')