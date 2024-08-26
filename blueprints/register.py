from exts import mail, db
from flask_mail import Message
from flask import render_template, Blueprint, request, jsonify, flash, session, redirect, url_for
import string, random
from models import Email_codetmp, User
from flask_login import login_user
from .confirm import ConfirmForm

bp = Blueprint('register', __name__)

def random_qr():
    source = string.digits*4
    codetmp = random.sample(source, 4)
    codetmp = ''.join(codetmp)
    return codetmp

def validate_user(email):
    if not email or '@' not in email:
        return False, 'Invalid email format'
    user_exist = User.query.filter_by(email=email).first()
    existemail = Email_codetmp.query.filter_by(email=email).first()
    if user_exist is not None and existemail is None:
        ## 用户存在才发送验证码
        return True, 'User already exists, code has sent'
    else:
        return False, 'User does not exist or Code has sent'

def validate_email(email):
    if not email or '@' not in email:
        return False, 'Invalid email format'
    existemail = Email_codetmp.query.filter_by(email=email).first()
    user_exist = User.query.filter_by(email=email).first()
    if user_exist is not None:
        return False, 'User already registered'
    if existemail is not None:
        return False, 'Code already sent'
    else:
        return True, 'success'

def send_db(message, codetmp, email, reset_flag = False):
    mail.send(message)
    print('QR code has sent successfully!')
    email_codetmp = Email_codetmp(codetmp=codetmp, email=email, reset_flag = reset_flag)
    db.session.add(email_codetmp)
    db.session.commit()

@bp.route('/register/email', methods=['POST'])
def get_codetmp():
    action = request.form.get("action")
    codetmp = random_qr()
    email = request.form.get("email")
    if action == 'register':
        is_valid, message = validate_email(email)
        if not is_valid:
            # 如果邮箱已经注册，返回错误消息
            return jsonify({'code': 400, 'message': message})
        message = Message('Hi', recipients=[email], body=f'您的验证码是:{codetmp}')
        send_db(message, codetmp, email)
        return jsonify({'code': 200, 'message': message})

    elif action == 'reset_pw':
        is_valid, message = validate_user(email)
        if not is_valid:
            # 如果用户不存在，返回错误信息
            return jsonify({'code': 400, 'message': message})
        message = Message('Hi', recipients=[email], body=f'您正在重置密码，验证码是:{codetmp}')
        reset_flag = True
        send_db(message, codetmp, email, reset_flag)
        return jsonify({'code': 200, 'message': message})

    else:
        return jsonify({'code': 400, "message": "Invalid action？"})

def reset_user(email):
    return Email_codetmp.query.filter_by(email=email, reset_flag=True).first()

@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        print('qiguia')
        return render_template("register.html")
    else:
        email = request.form.get("email")
        form = ConfirmForm(request.form)
        tmp = reset_user(email)
        print(email, tmp,"分注册与重置?")
        # TODO 区分注册与重置密码
        if form.validate():
            if tmp is None:
                ## 重置密码的用户不存在，则注册用户
                email = form.email.data
                password = form.password.data
                username = form.username.data
                user = User(email=email, username = username)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                print("我在注册注册")
                flash("注册成功！")
                return jsonify({'code': 200, 'redirect_url': url_for('admin.login')})
            else:

                ## 对用户的密码进行修改
                user = User.query.filter_by(email=email).first()
                password = form.password.data
                user.username = form.username.data
                user.set_password(password)
                db.session.commit()
                print(user.username, password, tmp)
                flash("密码修改成功！")
                return jsonify({'code': 200, 'redirect_url': url_for('admin.login')})
        else:
            errors = form.errors
            # 获取表单中的数据以便于前端重填
            form_data = {
                'email': form.email.data,
                'username': form.username.data,
                'password': form.password.data,
                'password_repeat': form.password_repeat.data,
            }
            return jsonify({'code': 400, 'errors': errors, 'form_data': form_data})


