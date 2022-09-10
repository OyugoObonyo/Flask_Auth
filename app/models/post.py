from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(120))
    author_email = db.Column(db.String(50), db.ForeignKey('user.email'), nullable=False) 