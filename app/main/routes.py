from flask import render_template, flash, redirect, url_for, request, g, current_app, json,app
from flask_login import login_user, logout_user, current_user, login_required
from app.main import bp
from flask_babel import _, get_locale
from flask import session
from app import babel
from flask import app




@bp.route('/language/<language>')
def language(language=None):
    session['language'] = language
    return redirect(url_for('main.index'))




@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():





	return render_template('index.html')