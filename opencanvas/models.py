from opencanvas import db


class User(db.Model):
    # id_ = db.Coloumn(db.Integer, primary_key=True)
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)

    pixel = db.relationship('Pixel', backref='username', lazy=True)

    def __repr__(self):
        return f"{self.username} {self.password}"


class Canvas(db.Model):
    width = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"{self.width} {self.height}"


class Pixel(db.Model):
    x = db.Column(db.Integer, primary_key=True)
    y = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String, nullable=False)
    user = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)

    def __repr__(self):
        return f"{self.x} {self.y} {self.color}"