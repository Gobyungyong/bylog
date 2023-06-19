from flask import Blueprint, render_template, url_for, session, request, g, flash, make_response
from werkzeug.utils import redirect
from bylog.models import User, Diary, Guest_book
from bylog import db
from datetime import datetime
from bylog.forms import Guest_bookForm, BlogForm
from bylog.views.auth_views import login_required

bp = Blueprint('main', __name__, url_prefix='/')
    
@bp.route('/')
def index():
    if 'user_id' in session:
        id = session['user_id']
        return redirect(url_for('main.bylog', id=id))
    else :
        return redirect(url_for('auth.login'))

@bp.route('/bylog/<int:id>',methods=("GET","POST"))
@login_required
def bylog(id):
    form = Guest_bookForm()
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    user = User.query.get(id)
    diary = Diary.query.filter_by(user_id = id).order_by(Diary.create_date.desc())
    guest = Guest_book.query.filter_by(blog=id).order_by(Guest_book.create_date.desc())
    blogcode = user.private_key
    
    if kw:
        search = '%%{}%%'.format(kw)
        diary = db.session.query(Diary).filter(Diary.subject.ilike(search) | 
                    Diary.content.ilike(search)
                ).order_by(Diary.create_date.desc())
    
    diary = diary.paginate(page=page, per_page=10)

    if request.method == 'POST' and form.validate_on_submit():
        guestbook = Guest_book(content=form.content.data, create_date=datetime.now(), user_id=g.user.id,user_name=g.user.username, blog=id)
        db.session.add(guestbook)
        db.session.commit()

    try:
        if id == session['user_id'] or session['user_id'] == 1 or session['code'] == blogcode:
            return render_template('main/base.html',user=user,diary=diary,kw=kw,form=form,guest=guest,id=id )
        elif 'user_id' in session:
            return redirect(url_for('main.bylog', id=session['user_id']))
    except:
        if 'user_id' not in session:
            return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))
        
#리팩토링
# @bp.route('/bylog/<int:id>')
# def bylog(id):
#     user = User.query.get(id)
#     try:
#         if id == session['user_id'] or session['user_id'] == 1:
#             return render_template('main/base.html',user=user)
#         elif session['user_id]:
#             return redirect(url_for('main.bylog', id=session['user_id']))
#     except:
#         return redirect(url_for('main.index'))

@bp.route('/delete/<int:guest_id>')
@login_required
def delete(guest_id):
    guest = Guest_book.query.get_or_404(guest_id)
    if g.user.id == guest.blog or g.user.id == 1 or g.user.id == guest.user_id:        
        db.session.delete(guest)
        db.session.commit()
        return redirect(url_for('main.bylog',id=guest.blog))
    else:
        flash('삭제권한이 없습니다')
        return redirect(url_for('main.bylog', id=guest.blog))
    
@bp.route('/redirecting/<int:id>', methods=("GET","POST"))
@login_required
def redirecting(id):
    user = User.query.get(id)
    form = BlogForm()
    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                code = form.blog.data
                master = User.query.filter_by(private_key = code).first()
                session['code'] = code
                return redirect(url_for('main.bylog', id = master.id))
        except:
            return render_template('main/redirecting.html',user=user, form=form)
    else:
        return render_template('main/redirecting.html',user=user, form=form)
    return render_template('main/redirecting.html',user=user, form=form)