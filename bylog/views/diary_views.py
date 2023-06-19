from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from datetime import datetime

from .. import db
from bylog.models import Diary, Comment, User
from bylog.forms import DiaryForm,CommentForm

from bylog.views.auth_views import login_required


bp = Blueprint('diary', __name__, url_prefix='/diary')

@bp.route('/create/<int:user_id>', methods=('GET','POST'))
@login_required
def create(user_id):
    form = DiaryForm()
    user = User.query.get(user_id)
    if request.method == 'POST' and form.validate_on_submit():
        diary = Diary(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user_id=user_id, private = form.private.data )
        db.session.add(diary)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('diary/diary_form.html', form=form,user=user) 

@bp.route('/detail/<int:diary_id>/')
@login_required
def detail(diary_id):
    form = CommentForm()
    diary = Diary.query.get_or_404(diary_id)
    user = User.query.get(diary.user_id)
    return render_template('diary/diary_detail.html', diary=diary,user=user,form=form) 

@bp.route('/modify/<int:diary_id>/', methods=("GET","POST"))
@login_required
def modify(diary_id):
    diary = Diary.query.get_or_404(diary_id)
    user = g.user
    if user != diary.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('diary.detail', diary_id=diary_id))
    if request.method == 'POST':
        form = DiaryForm()
        if form.validate_on_submit():
            form.populate_obj(diary)
            diary.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('diary.detail', diary_id=diary_id))
    else:
        form = DiaryForm(obj=diary)
        print(diary.content)
    return render_template('diary/diary_form.html', form=form, user=user) 

@bp.route('/delete/<int:diary_id>')
@login_required
def delete(diary_id):
    diary = Diary.query.get_or_404(diary_id)
    if g.user == diary.user or g.user.id == 1:
        db.session.delete(diary)
        db.session.commit()
        return redirect(url_for('main.bylog',id=diary.user_id))
    else:
        flash('삭제권한이 없습니다')
        return redirect(url_for('diary.detail', diary_id=diary_id))