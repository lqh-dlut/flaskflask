import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import User, Email_codetmp
from exts import db

class ConfirmForm(wtforms.Form):


    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    codetmp = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=1, max=20, message="密码格式错误！")])
    password_repeat = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])

    def validate_email(self, field):
        email = field.data
        reset = Email_codetmp.query.filter_by(reset_flag=True, email=email).first()
        user = User.query.filter_by(email=email).first()
        if reset:
            ## 重置密码的用户不需要判断是否存在
            pass
        elif user:
            #如果查询到邮箱已存在
            raise wtforms.ValidationError(message="邮箱已经被注册！")

    def validate_codetmp(self, field):
        codetmp = self.codetmp.data
        email = self.email.data
        print(codetmp, email)
        codetmp_obj = Email_codetmp.query.filter_by(email=email, codetmp=codetmp).first()
        if not codetmp_obj:
            raise wtforms.ValidationError(message="邮箱或验证码错误！")
        else:
            db.session.delete(codetmp_obj)
            # db.session.commit()


