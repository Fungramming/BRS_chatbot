from . import db, login
from flask_login import UserMixin


class Mall(db.Model, UserMixin):
    __tablename__ = 'mall'
    id = db.Column(db.Integer, primary_key=True)
    mall_id = db.Column(db.String, unique=True)
    shop_no = db.Column(db.Integer, default=1)
    is_multi_shop = db.Column(db.String, default=None)
    lang = db.Column(db.String, default='ko_KR')
    access_token = db.Column(db.String, default=None)
    refresh_token = db.Column(db.String, default=None)
    expires_at = db.Column(db.DateTime, default=None)
    refresh_token_expires_at = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return '<Mall {}>'.format(self.mall_id)


@login.user_loader
def load_user(id):
    return Mall.query.get(int(id))


login.login_message = None

