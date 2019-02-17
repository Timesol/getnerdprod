from flask import render_template, flash, redirect, url_for, request, g, current_app, json,app,jsonify, Response
from flask_login import login_user, logout_user, current_user, login_required
from app.main import bp
from flask_babel import _, get_locale
from flask import session
from app import babel
from flask import app
from app.models import Task,City,User
from app.main.forms import TaskForm
from app import db
import os
from werkzeug.utils import secure_filename
from flask_babel import gettext, ngettext
from jinja2 import Template

@bp.route('/language/<language>')
def language(language=None):
    session['language'] = language
    return redirect(url_for('main.index'))





@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index(city=None):
    
    city=City.query.filter_by(name=city).first()
    


    available_citys=City.query.all()
    folder=os.environ.get('ICON_FOLDER')
    filelist=[]
    for x in os.listdir(folder):
        filelist.append(x)
    citys_list=[(i.id,i.name) for i in available_citys]
    
    form_task=TaskForm()
    
    form_task.city.choices = citys_list
    
    
    if form_task.validate_on_submit():
        print('in form')
        city=City.query.get(form_task.city.data)
        print('in form')                
        task = Task(body=form_task.body.data, author=current_user,
            internet=form_task.internet.data, summary=form_task.summary.data,price=form_task.price.data,currency=form_task.currency.data, status='open')       
        db.session.add(task)
        db.session.commit()      
        scity=City.query.get(form_task.city.data)
        scity.citytasks.append(task)
        db.session.commit()
        return redirect(url_for('main.index'))

    
        
        
        
        

    
            
        page = request.args.get('page', 1, type=int)
        
        tasks = city.citytasks.order_by(Task.timestamp.desc()).paginate(
            page, current_app.config['TASKS_PER_PAGE'], False)
        next_url = url_for('main.index', page=tasks.next_num) \
            if tasks.has_next else None
        prev_url = url_for('main.index', page=tasks.prev_num) \
            if tasks.has_prev else None
    else:
        page = request.args.get('page', 1, type=int)
        tasks = Task.query.order_by(Task.timestamp.desc()).paginate(
            page, current_app.config['TASKS_PER_PAGE'], False)
        next_url = url_for('main.index', page=tasks.next_num) \
            if tasks.has_next else None
        prev_url = url_for('main.index', page=tasks.prev_num) \
            if tasks.has_prev else None

  
        





    return render_template('index.html',tasks=tasks.items, next_url=next_url,
                           prev_url=prev_url, form_task=form_task,filelist=filelist)


@bp.route('/index_r', methods=['GET', 'POST'])
def index_r(city=None):

    
        page = request.args.get('page', 1, type=int)
        tasks = Task.query.order_by(Task.timestamp.desc()).paginate(
            page, current_app.config['TASKS_PER_PAGE'], False)
        next_url = url_for('main.index', page=tasks.next_num) \
            if tasks.has_next else None
        prev_url = url_for('main.index', page=tasks.prev_num) \
            if tasks.has_prev else None
        return render_template('_index.html',tasks=tasks.items, next_url=next_url,
                           prev_url=prev_url)





@bp.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():

    


    return render_template('add_task.html')


@bp.route('/task/<id>', methods=['GET', 'POST'])
@login_required

def task(id):
    task= Task.query.get(id)
    



    return render_template('task.html' ,task=task)


@bp.route('/take_task', methods=['GET', 'POST'])
@login_required
def take_task():

    if request.method == 'POST':
        task_id=request.form.get('id', None)
        task=Task.query.get(task_id)
        if task.status == 'open' and current_user.tasks_taken.count() <= 3:
            task.status='progress'
            current_user.tasks_taken.append(task)
            db.session.commit()
        else:
            if current_user.tasks_taken.count() >= 3:
                
                message= _('You can\'t take more than 3 tasks!')
            else:

                message=_('Task already taken!')
        
       


        
        return json.dumps({'status':'OK','message':message});


@bp.route('/remove_task', methods=['GET', 'POST'])
@login_required
def remove_task():

    if request.method == 'POST':
        task_id=request.form.get('id', None)
        task=Task.query.get(task_id)
        if task.author== current_user or task.user == current_user:
            task.status='open'
            current_user.tasks_taken.remove(task)
            db.session.commit()

        elif  task.status== 'progress':
            message=_('Only the Creator or Task taker can change a task!')
        
       


        
        return json.dumps({'status':'OK','message':message});


@bp.route('/close_task', methods=['GET', 'POST'])
@login_required
def close_task():

    if request.method == 'POST':
        task_id=request.form.get('id', None)
        task=Task.query.get(task_id)

        if task.author== current_user or task.user == current_user:
            task.status='closed'
            db.session.commit()
        else:
            message=_('Only the Creator or Task taker can change a task!')
        
        
       


        
        return json.dumps({'status':'OK','message':message});