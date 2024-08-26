from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from exts import db

bp = Blueprint('setting', __name__)


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        current_user.name = name
        # 等同于 user = User.query.first()
        #       user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')