from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import functools

from bylog import db
from bylog.forms import UserCreateForm, UserLoginForm, UserModifyForm
from bylog.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        key = User.query.filter_by(private_key=form.private_key.data).first()
        if not user and not key:
            user = User(username = form.username.data,
                        password = generate_password_hash(form.password1.data),
                        email = form.email.data,
                        private_key = form.private_key.data,
                        introduction = f'환영합니다. {form.username.data}의 BYlog입니다.')
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        elif user and key:
            flash('이미 존재하는 이메일입니다.')
            flash('이미 존재하는 블로그코드입니다.')
        elif key:
            flash('이미 존재하는 블로그코드입니다.')
        elif user:
            flash('이미 존재하는 이메일입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login', methods=('GET','POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(email = form.email.data).first()
        if not user:
            error = '존재하지 않는 사용자입니다.'
        elif not check_password_hash(user.password, form.password.data):
            error = '비밀번호가 올바르지 않습니다.'
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.bylog',id=user.id))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
        
@bp.route('/admin/')
@login_required
def admin():
    page = request.args.get('page',type=int,default=1)
    kw = request.args.get('kw', type=str, default='')
    user = User.query.order_by(User.id)
   
    # kw있으면 user db에서 이름,블로그코드,이메일이랑 매칭되는것들 user에 할당
    if kw:
        search = '%%{}%%'.format(kw)
        user = db.session.query(User).filter(User.username.ilike(search) |
                    User.email.ilike(search) | 
                    User.private_key.ilike(search))
    
    user = user.paginate(page=page,per_page=25)
    
    try:
        if session['user_id'] == 1:
            return render_template('auth/admin.html',user=user,kw=kw)
        elif 'user_id' in session:
            return redirect(url_for('main.index'))
    except:
        if 'user_id' not in session:
            return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))
        
@bp.route('/modify/<int:id>', methods=("GET","POST"))
@login_required
def modify(id):
    user = User.query.get(id)
    form = UserModifyForm()

    if request.method == 'POST' and form.validate_on_submit(): #POST
        key = User.query.filter_by(private_key=form.private_key.data).first()
        pswd = form.password1.data
        blog = form.private_key.data
        
        if not pswd and blog: # 비밀번호 변경x
            user.introduction = form.introduction.data
            user.private_key = form.private_key.data
            db.session.commit()
            return redirect(url_for('main.bylog', id=id))
        elif not key and not pswd and not blog: # 비밀번호 변경
            user.introduction = form.introduction.data
            db.session.commit()
            return redirect(url_for('main.bylog', id=id))
        elif pswd and blog: # 비밀번호 변경x
            user.password = generate_password_hash(form.password1.data)
            user.introduction = form.introduction.data
            user.private_key = form.private_key.data
            db.session.commit()
            return redirect(url_for('main.bylog', id=id))
        elif not key and pswd and not blog: # 비밀번호 변경x
            user.password = generate_password_hash(form.password1.data)
            user.introduction = form.introduction.data
            db.session.commit()
            return redirect(url_for('main.bylog', id=id))
        elif key: #블로그코드 중복
            flash('이미 존재하는 블로그코드입니다.')
        return redirect(url_for('auth.modify', id=id)) 
    
    else: #GET
        try:
            if id == session['user_id'] or session['user_id'] == 1: #본인/관리자만 진입가능
                return render_template('auth/modify.html',user=user, form=form, id=id)
            elif 'user_id' in session:
                return redirect(url_for('auth.modify', id=session['user_id'])) #타인 회원정보수정 접근 시 본인 정보수정으로 보내기
        except:
            if 'user_id' not in session:
                return redirect(url_for('main.index')) #비로그인 로그인페이지로
    return redirect(url_for('main.index')) #비로그인 로그인페이지로