from app import db

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    social_platform = db.Column(db.String(20), nullable=False)
    account_url = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(120), nullable=False)
    reporter_email = db.Column(db.String(50), db.ForeignKey('user.email'), nullable=False)