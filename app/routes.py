# -*- coding: utf-8 -*-
from flask import render_template,flash, redirect, request
from flask_login import LoginManager, UserMixin, logout_user, login_required, login_user, current_user 
from app import app,con
from werkzeug.security import generate_password_hash, check_password_hash 
from app.forms import LoginForm
from app.forms import RegisterForm,AddWorkForm,AddConferenceForm,Works,IndexForm


login_manager = LoginManager() 
login_manager.init_app(app) 
login_manager.login_view = "login" 

class User(UserMixin): 
 def __init__(self, id): 
  self.id = id 
  self.role = str
  self.username = str
  self.group = str
 def __repr__(self): 
  return "%d/%s/%s/%s/%d" % (self.id) 

@login_manager.user_loader 
def load_user(user_id): 
  return User(user_id) 

cur = con.cursor()

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required 
def index():
     cur.execute('select username, email, type_u from Пользователи where id = %s',(current_user.id,))
     user1 = cur.fetchone()
     st_gr = user1
     if user1[2] == 'Студент':
      cur.execute('select №Группы from Студент where email = %s',(user1[1],))
      st_gr = cur.fetchone()
     user = {'username' : user1[0], 'role' : user1[2], 'group' : st_gr[0]}
     form = IndexForm()
     cur.execute('select ФИО, №Зачетки,Стипендия,№Группы from Студент order by ФИО')
     students = cur.fetchall()
     if user1[2] == 'Студент':
      cur.execute('select №Зачетки from Студент where ФИО = %s',(user1[0],))
      s_number = cur.fetchone()
      cur.execute('select НаучнаяРабота.Название, ТемаНаучнаяРабота.НазваниеТемы, НаучнаяРабота.ФИОНаучрук from НаучнаяРабота, ТемаНаучнаяРабота where НаучнаяРабота.Название = ТемаНаучнаяРабота.НазваниеРаботы and НаучнаяРабота.Название in (select Название from СтудентНаучнаяРабота where №Зачетки = %s);',(s_number))
     elif user1[2] == 'Преподаватель':
      cur.execute('select НаучнаяРабота.Название, ТемаНаучнаяРабота.НазваниеТемы, НаучнаяРабота.ФИОНаучрук from НаучнаяРабота, ТемаНаучнаяРабота where НаучнаяРабота.Название = ТемаНаучнаяРабота.НазваниеРаботы and НаучнаяРабота.Название in (select Название from НаучнаяРаботаПрепод where ФИО = %s);',(user1[0],))  
     w = cur.fetchall()
     w1 = cur.fetchall()
     w_prep = cur.fetchall()
     w_st = cur.fetchall()
     if user1[2] == 'Преподаватель':
        cur.execute('select НазваниеРаботы, НазваниеТемы from ТемаНаучнаяРабота where НазваниеРаботы in (select Название from НаучнаяРабота where ФИОНаучрук = %s)',(user1[0],))
        w1 = cur.fetchall()
        cur.execute('select * from НаучнаяРаботаПрепод')
        w_prep = cur.fetchall()
        cur.execute('select СтудентНаучнаяРабота.Название, Студент.ФИО from СтудентНаучнаяРабота, Студент where СтудентНаучнаяРабота.№Зачетки = Студент.№Зачетки')
        w_st = cur.fetchall()
     if form.validate_on_submit():
        if form.submit.data == True:
         if form.group.data == '':
          flash('Вы не ввели номер группы!')
          return redirect('/index')
         cur.execute('select * from Группа where №Группы = %s;',(form.group.data,))
         g = cur.fetchone()
         if g is None:
             cur.execute('insert into Группа values (%s);',(form.group.data,))
             con.commit()
             flash('Группа добавлена!')
             return redirect('/index')
         else:
             flash('Такая группа уже существует!')
             return redirect('/index')
        elif form.submit_s.data == True:
           if form.grant.data =='':
            form.grant.data = 0
           if int(form.grant.data) == 0:
            cur.execute('update Студент set Стипендия = %s where №Зачетки = %s',(None,form.s_num.data,))
           else:
            cur.execute('update Студент set Стипендия = %s where №Зачетки = %s',(form.grant.data,form.s_num.data,))
           con.commit()
           flash('Стипендия изменена!')
           return redirect('/index')
        elif form.submit_st_del.data == True:
        	cur.execute('select email from Студент where №Зачетки = %s',(form.st_del_id.data,))
        	email = cur.fetchone()
        	cur.execute('delete from СтудентНаучнаяРабота where №Зачетки = %s',(form.st_del_id.data,))
        	cur.execute('delete from Студент where №Зачетки = %s',(form.st_del_id.data,))
        	cur.execute('delete from Пользователи where email = %s',(email,))
        	con.commit()
        elif form.gr_del.data == True:
          cur.execute('select ФИО from Студент where №Группы = %s',(form.gr_del_num.data,))
          st_in_gr = cur.fetchone()
          if st_in_gr is None:
            cur.execute('delete from Группа where №Группы = %s',(form.gr_del_num.data,))
            con.commit()
          else:
            flash('В этой группе еще продолжают учиться студенты!')
        elif form.prep_del_s.data == True:
         cur.execute('delete from НаучнаяРаботаПрепод where ФИО = %s',(form.prep_del.data,))
         cur.execute('select Название from НаучнаяРабота where ФИОНаучрук = %s',(form.prep_del.data,))
         prep_del = cur.fetchone()
         if prep_del is not None:
          cur.execute('delete from СтудентНаучнаяРабота where Название in (select Название from НаучнаяРабота where ФИОНаучрук = %s)',(form.prep_del.data,))
          cur.execute('delete from Участие where НазваниеРаботы in (select Название from НаучнаяРабота where ФИОНаучрук = %s)',(form.prep_del.data,))
          cur.execute('delete from ТемаНаучнаяРабота where НазваниеРаботы in (select Название from НаучнаяРабота where ФИОНаучрук = %s)',(form.prep_del.data,))
          cur.execute('delete from НаучнаяРабота where ФИОНаучрук = %s',(form.prep_del.data,))
         cur.execute('delete from Преподаватель where ФИО = %s',(form.prep_del.data,))
         cur.execute('delete from Пользователи where username = %s',(form.prep_del.data,))
         flash('Преподаватель %s уволен!',(form.prep_del.data))
     cur.execute('select ФИО, №Зачетки,Стипендия,№Группы from Студент order by ФИО')
     students = cur.fetchall()
     cur.execute('select * from Преподаватель')
     prep = cur.fetchall()
     cur.execute('select * from Группа order by №Группы')
     gr = cur.fetchall()
     return render_template('index.html', title='Научные работы', user=user, form=form, w=w, w1=w1, students=students, w_prep=w_prep, w_st=w_st, gr=gr, prep=prep)

@app.route('/logout') 
@login_required 
def logout(): 
 logout_user() 
 flash('Вы вышли из профиля') 
 return redirect('login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Вы уже вошли в ученую запись!')
        return redirect('index')
    user = [None,None]
    form = LoginForm()
    if form.validate_on_submit():
        cur.execute('select id,email,pass_hash,type_u from Пользователи where email = %s',(form.username.data,))
        user = cur.fetchone()
        if user is None:
           flash('Такого пользователя не существует!')
           return redirect('login')
        if not check_password_hash(user[2], form.password.data):
           flash('Неправильный пароль!')
           return redirect('login')
        id = user[0]
        user_id = User(id)
        login_user(user_id, remember = form.remember_me.data)
        flash('Добро пожаловать')
        return redirect('index')
    return render_template('login.html', title='Вход', form=form, user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
   if current_user.is_authenticated:
        flash('Вы уже вошли в ученую запись!')
        return redirect('index')
   user = [None,None]
   form = RegisterForm()
   cur.execute('select * from Группа order by №Группы')
   gr = cur.fetchall()
   if form.validate_on_submit():
        cur.execute('select email from Пользователи where email = %s;',(form.email.data,))
        check_user = cur.fetchone()
        if check_user is not None:
           flash ('Эта почта уже зарегистрирована!')         
           return redirect('register')
        if form.role.data == 'Преподаватель':
         if form.position.data == "" or form.department_number.data == "":
            flash('Вы не полностью заполнили форму!')
            return redirect('register')
         elif type(form.department_number.data) != int:
            flash('Номер кафедры указан неверно!')
            return redirect('register')
         else:
            cur.execute('insert into Преподаватель (email, ФИО, №Кафедры, Должность, Звание) values (%s,%s,%s,%s,%s);',(form.email.data,form.username.data,form.department_number.data,form.position.data, form.rank.data))
            con.commit()
        if form.role.data == 'Студент':
            cur.execute('select №Группы from Группа where №Группы = %s',(form.group_num.data,))
            st_gr = cur.fetchone()
            if form.record_num.data =="" or form.group_num.data == "":
              flash('Вы не полностью заполнили формуу!')
              return redirect('register')
            elif st_gr is None:
             flash('Такой группы не существует!')
             return redirect('register')
            else:
             cur.execute('insert into Студент (email, ФИО, №Зачетки, №Группы) values (%s,%s,%s,%s);',(form.email.data,form.username.data,form.record_num.data,form.group_num.data))
             con.commit()
        cur.execute('insert into Пользователи (username, pass_hash, email, type_u) values (%s,%s,%s,%s);',(form.username.data,generate_password_hash(form.password1.data),form.email.data,form.role.data))
        cur.execute('select id from Пользователи where email = %s',(form.username.data,))
        user = cur.fetchone()
        con.commit()
        id = user
        user_id = User(id)
        flash ('Вы успешно зарегистрировались!')
        return redirect('login')
   return render_template('register.html', title='Регистрация', form=form, user=user, gr=gr)

@app.route('/add_work', methods=['GET', 'POST'])
@login_required
def add_work():
    cur.execute('select Название from Тема')
    theme = cur.fetchall()
    cur.execute('select НазваниеТемы, НазваниеКонференции from ТемаКонференция')
    theme_conf = cur.fetchall()
    cur.execute('select НазваниеКонференции, Номер from ПроведениеКонференции')
    conf_num = cur.fetchall()
    cur.execute('select username, email, type_u from Пользователи where id = %s',(current_user.id,))
    user1 = cur.fetchone()
    user = {'username' : user1[0], 'role' : user1[2]}
    form = AddWorkForm()
    if form.validate_on_submit():
        cur.execute('select НазваниеТемы, НазваниеКонференции from ТемаКонференция where (НазваниеКонференции = %s) and (НазваниеТемы = %s);',(form.conference.data,form.theme.data,))
        us = cur.fetchone()
        if us is None:
            flash('Вы не можете заявить работу с такой темой на указанную конференцию!')
            return redirect('add_work')
        cur.execute('select * from НаучнаяРабота where Название = %s and ФИОНаучрук = %s;',(form.title.data,user1[0],))
        us = cur.fetchone()
        if us is None:
         cur.execute('insert into НаучнаяРабота values (%s,%s);',(form.title.data,user1[0],))
        cur.execute('insert into ТемаНаучнаяРабота values (%s,%s);',(form.title.data,form.theme.data,))
        cur.execute('select Дата from ПроведениеКонференции where НазваниеКонференции = %s;',(form.conference.data,))
        us = cur.fetchone()
        cur.execute('insert into Участие (НазваниеРаботы, НомерКонференции, Дата, НазваниеКонференции) values (%s,%s,%s,%s);',(form.title.data,form.conference_number.data,us,form.conference.data,))
        con.commit()
        flash('Работа успешно добавлена!')
        return redirect('/index')
    return render_template('add_work.html', title='Новая научная работа',form=form, user=user, theme_conf=theme_conf, conf_num=conf_num, theme=theme)

@app.route('/add_conference', methods=['GET', 'POST'])
@login_required
def add_conference():
    cur.execute('select username, email, type_u from Пользователи where id = %s',(current_user.id,))
    user1 = cur.fetchone()
    user = {'username' : user1[0], 'role' : user1[2]}
    form = AddConferenceForm()
    if form.validate_on_submit():
        cur.execute('select Название from Конференция where Название = %s;',(form.title.data,))
        r = cur.fetchone()
        if r is None:
         cur.execute('insert into Конференция values (%s);',(form.title.data,))
        cur.execute('insert into ПроведениеКонференции values (%s,%s,%s);',(form.number.data,form.date.data,form.title.data,))
        cur.execute('select Название from Тема where Название = %s;',(form.theme.data,))
        r = cur.fetchone()
        if r is None:
         cur.execute('insert into Тема values (%s);',(form.theme.data,))
        cur.execute('select * from ТемаКонференция where НазваниеТемы = %s and НазваниеКонференции = %s;',(form.theme.data,form.title.data,))
        r = cur.fetchone()
        if r is None:
         cur.execute('insert into ТемаКонференция values (%s,%s);',(form.theme.data,form.title.data,))
        con.commit()
        flash('Конференция успешно добавлена!')
        return redirect('/index')
    return render_template('add_conference.html', title='Добавление конференции', form=form, user = user)

@app.route('/works', methods=['GET', 'POST'])
@login_required 
def works():     
     cur.execute('select username, email, type_u from Пользователи where id = %s',(current_user.id,))
     user1 = cur.fetchone()
     user = {'username' : user1[0], 'role' : user1[2]}
     cur.execute('select type_u,username from Пользователи where id=%s',(current_user.id,))
     r = cur.fetchall()
     if r[0][0] == 'Студент':
      cur.execute('select №Зачетки from Студент where ФИО = %s',(r[0][1],))
      s_number = cur.fetchone()
     cur.execute('select distinct НаучнаяРабота.Название, ТемаНаучнаяРабота.НазваниеТемы, НаучнаяРабота.ФИОНаучрук from НаучнаяРабота, ТемаНаучнаяРабота where НаучнаяРабота.Название = ТемаНаучнаяРабота.НазваниеРаботы;')
     w = cur.fetchall()
     if r[0][0] == 'Студент':
      cur.execute('select * from СтудентНаучнаяРабота')
     elif r[0][0] == 'Преподаватель':
      cur.execute('select Название from НаучнаяРаботаПрепод where ФИО = %s',(r[0][1],))
     check = cur.fetchone()    
     form = Works()
     if form.validate_on_submit():
        cur.execute('select type_u,username from Пользователи where id=%s',(current_user.id,))
        r = cur.fetchall()
        if r[0][0] == 'Преподаватель':
            cur.execute('insert into НаучнаяРаботаПрепод values (%s,%s)',(form.names.data,r[0][1],))
        elif r[0][0] == 'Студент':
            cur.execute('insert into СтудентНаучнаяРабота values (%s,%s)',(form.names.data,s_number,))
        con.commit()
        return redirect('/index')
     return render_template('works.html', title='Принять участие в научной работе', user=user, w=w, form=form, r=r, check=check)