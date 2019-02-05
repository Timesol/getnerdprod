from flask import render_template, flash, redirect, url_for, request, g, current_app, json
from flask_login import login_user, logout_user, current_user, login_required
from app.main import bp
from flask_babel import _, get_locale
from flask import session


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = 'en'

@bp.route('/langchange/<lang>')
def set_language(language=None):
    session['lang'] = lang
    return True


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():





	return render_template('index.html')