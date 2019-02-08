from flask import render_template, flash, redirect, url_for, request, g, current_app, json,app
from flask_login import login_user, logout_user, current_user, login_required
from app.main import bp
from flask_babel import _, get_locale
from flask import session
from app import babel
from flask import app
from app.models import Task,City,User
from app.main.forms import TaskForm
from app import db




@bp.route('/language/<language>')
def language(language=None):
    session['language'] = language
    return redirect(url_for('main.index'))




@bp.route('/<city>', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index(city=None):
    
    city=City.query.filter_by(name=city).first()
    


    available_citys=City.query.all()
    citys_list=[(i.id,i.name) for i in available_citys]
    
    form_task=TaskForm()
    
    form_task.city.choices = citys_list
    
    
    if form_task.validate_on_submit():
                
                task = Task(body=form_task.body.data, author=current_user,
                    internet=form_task.internet.data, summary=form_task.summary.data)
        
                db.session.add(task)
                db.session.commit()
        
                scity=City.query.get(form_task.city.data)
                scity.citytasks.append(task)
                db.session.commit()

    if city is not None:
        
        
        
        

    
            
        page = request.args.get('page', 1, type=int)
        
        tasks = city.citytasks.paginate(
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
                           prev_url=prev_url, form_task=form_task)


@bp.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():

    


    return render_template('add_task.html')