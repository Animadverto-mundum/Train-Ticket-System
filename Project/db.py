from app import app
from model import *
from werkzeug.security import generate_password_hash

if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        db.create_all()
        reg_user = UserStaff(user_name='llb', password=generate_password_hash('llmnb'), department_type_number=0)
        db.session.add(reg_user)
        reg_user = UserStaff(user_name='zlb', password=generate_password_hash('zypnb'), department_type_number=1)
        db.session.add(reg_user)
        reg_user = UserStaff(user_name='wlb', password=generate_password_hash('wgtnb'), department_type_number=2)
        db.session.add(reg_user)
        reg_user = UserStaff(user_name='jlb', password=generate_password_hash('jjqnb'), department_type_number=3)
        db.session.add(reg_user)
        reg_user = UserStaff(user_name='slb', password=generate_password_hash('slbnb'), department_type_number=4)
        db.session.add(reg_user)
        reg_user = UserStaff(user_name='ylb', password=generate_password_hash('yzhnb'), department_type_number=5)
        db.session.add(reg_user)
        sql = ''.join(open('Testcase.sql', 'r').readlines()).split(';')
        for item in sql:
            db.session.execute(item + ';')
        db.session.commit()