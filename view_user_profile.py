from app import app
from exts import db
from models import User, Email_codetmp

def query_users():
    with app.app_context():
        users = User.query.all()
        # for mail in mails: print(mail)
        for user in users: print(user.username)
        # print(len(users))


def query_email():
    with app.app_context():
        emails = Email_codetmp.query.all()
        for email in emails:
            print(email.codetmp)
            print(email.email)


if __name__ == '__main__':
    query_email()
    query_users()