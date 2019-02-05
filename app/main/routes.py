from flask import render_template, flash, redirect, url_for, request, g, current_app, json,app
from flask_login import login_user, logout_user, current_user, login_required
from app.main import bp
from flask_babel import _, get_locale
from flask import session
from app import babel

@bp.context_processor
def inject_conf_var():
    return dict(
               AVAILABLE_LANGUAGES=current_app.config['LANGUAGES'],
               CURRENT_LANGUAGE=session.get('language',request.accept_languages.best_match(current_app.config['LANGUAGES'].keys())))


@bp.route('/language/<language>')
def set_language(language=None):
    session['language'] = language
    return redirect(url_for('index'))




@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():





	return render_template('index.html', AVAILABLE_LANGUAGES=AVAILABLE_LANGUAGES)