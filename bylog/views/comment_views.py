from datetime import datetime

from flask import Blueprint, url_for, request, g, flash
from werkzeug.utils import redirect

from bylog import db
from bylog.models import Diary,Comment
from bylog.forms import CommentForm

from bylog.views.auth_views import login_required


bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/<int:diary_id>', methods=('POST',))
@login_required
def create(diary_id):
    form = CommentForm()
    if form.validate_on_submit():
        diary = Diary.query.get_or_404(diary_id)
        content = request.form['content']
        comment = Comment(content=content, create_date=datetime.now(),user_id=g.user.id,user_name=g.user.username)
        diary.comment_set.append(comment)
        db.session.commit()
    else:
        flash('내용을 입력하세요!')
    return redirect(url_for('diary.detail', diary_id=diary_id,form=form))

@bp.route('/delete/<int:comment_id>')
@login_required
def delete(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    diary_id = comment.diary.id
    if g.user == comment.user or g.user.id == 1:
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('diary.detail', diary_id=diary_id))
    else:
        flash('삭제권한이 없습니다')