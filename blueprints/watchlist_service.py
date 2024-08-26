from flask import Blueprint, request, redirect, url_for, render_template, flash, abort
from models import Watchlist
from flask_login import login_required, current_user
from exts import db
import markdown

bp = Blueprint('watchlist', __name__)

@bp.route('/movie/file/<int:movie_id>')
def file(movie_id):
    movie = Watchlist.query.get_or_404(movie_id)
    return render_template('file.html', movie=movie)

@bp.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Watchlist.query.get_or_404(movie_id)
    print(movie_id, movie.filmnote)
    if request.method == 'POST':  # 处理编辑表单的提交请求

        title = request.form['title']
        year = request.form['year']
        filmnote = request.form['filmnote']
        if request.form.get('private_flag') is None:
            private_flag = False
        else:
            private_flag = True


        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('watchlist_service.edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        movie.filmnote = filmnote
        movie.private_flag = private_flag
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录

@bp.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required
def delete(movie_id):
    movie = Watchlist.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页
