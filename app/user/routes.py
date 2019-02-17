from app.user import bp
from flask import render_template, flash, redirect, url_for, request, g, current_app, json
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.models import User, Post,Task
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER_ENV')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx','cfg','svg'])
ALLOWED_EXTENSIONS_PANDAS = set(['xlsx'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file_pandas(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PANDAS
    return True  






@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    folder=os.environ.get('ICON_FOLDER')
    filelist=[]
    for x in os.listdir(folder):
        filelist.append(x)
    

    user = User.query.filter_by(username=username).first_or_404()
    
    tasks_created=user.tasks
    
    tasks_taken=user.tasks_taken
   

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part!')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file!')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder, filename))
            flash(_('File uploaded!'))
            
                
        return redirect(url_for('user.user',username=user.username, user=user,
                            filename=filename,filelist=filelist, ))

    return render_template('user.html', user=user, 
                            filelist=filelist,tasks_taken=tasks_taken ,tasks_created=tasks_created)


@bp.route('/tasks_taken_r', methods=['GET', 'POST'])
@login_required
def tasks_taken_r():


    tasks_taken=current_user.tasks_taken
    return render_template('_taken.html',tasks_taken=tasks_taken)


@bp.route('/tasks_created_r', methods=['GET', 'POST'])
@login_required
def tasks_created_r():


    tasks_created=current_user.tasks
    return render_template('_created.html',tasks_created=tasks_created)







@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('user.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('user.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('user.user', username=username))