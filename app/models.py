from . import db, login
from flask_login import UserMixin


class Mall(db.Model, UserMixin):
    __tablename__ = 'mall'
    id = db.Column(db.Integer, primary_key=True)
    mall_id = db.Column(db.String, unique=True)
    shop_no = db.Column(db.Integer, default=1)
    access_token = db.Column(db.String, default=None)
    expires_at = db.Column(db.DateTime, default=None)
    scripts = db.relationship('Script', backref='mall', lazy='dynamic')

    def __repr__(self):
        return '<Mall {}>'.format(self.mall_id)


@login.user_loader
def load_user(id):
    return Mall.query.get(int(id))


login.login_message = None


class Script(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    script_id = db.Column(db.String, unique=True)
    script_name = db.Column(db.String)
    mall_id = db.Column(db.Integer, db.ForeignKey('mall.id'))

    def __repr__(self):
        return '<Script {}>'.format(self.script_name)

